"""Customer routes.

UC-01 Place an order: choose hub -> dishes, address, voucher -> quote and payment choice ->
(online: payment simulator) -> confirm -> confirmation.
SUC-03 Track my orders and answer a replacement offer; SUC-04 Cancel an order.

Routes stay thin: they read the form, call the controller and render the result.
"""
import uuid

from flask import Blueprint, redirect, render_template, request, url_for

from saigonbite.business.controllers import (HubUnavailableError, OrderTrackingController, PaymentChoice,
                                             PaymentDeclinedError, PlaceOrderController, QuoteChangedError,
                                             ValidationError)
from saigonbite.business.domain import OnlineOption, PaymentMethod, Role
from saigonbite.data_access import APPROVE, DECLINE
from saigonbite.presentation.auth import role_required
from saigonbite.presentation.db import get_db
from saigonbite.presentation.helpers import act, uid

bp = Blueprint("order", __name__, url_prefix="/order")


def _controller() -> PlaceOrderController:
    return PlaceOrderController(get_db())


def _tracking() -> OrderTrackingController:
    return OrderTrackingController(get_db())


def _read_quantities(form) -> dict[int, str]:
    """Collect qty_<menu_item_id> fields. Raw strings: the controller validates them."""
    return {int(k[4:]): v for k, v in form.items() if k.startswith("qty_") and k[4:].isdigit()}


def _read_payment(form) -> PaymentChoice:
    """payment = COD or ONLINE:<option>; sim_outcome = the simulator's answer, if it was shown."""
    raw = form.get("payment", "COD")
    method, _, option = raw.partition(":")
    try:
        choice = PaymentChoice(method=PaymentMethod(method),
                               option=OnlineOption(option) if option else None)
    except ValueError:
        raise ValidationError("Please choose how to pay.") from None
    if choice.method is PaymentMethod.ONLINE and choice.option is None:
        raise ValidationError("Please choose how to pay.")
    outcome = form.get("sim_outcome")
    choice.outcome = outcome if outcome in (APPROVE, DECLINE) else None
    return choice


def _render_hubs(error: str | None, suggestions=None, status: int = 200):
    return render_template("order/hubs.html", hubs=_controller().list_hubs(), error=error,
                           suggestions=suggestions or []), status


def _render_menu(hub_id: int, error: str | None, quantities: dict[int, str], address_id, voucher_code, status: int):
    try:
        view = _controller().select_hub(uid(), hub_id)
    except ValidationError as exc:           # unknown or archived hub
        return _render_hubs(str(exc), status=400)
    groups: dict[str, list] = {}                 # brands in menu order, not alphabetical
    for entry in view.menu:
        groups.setdefault(entry.item.brand_name, []).append(entry)
    return render_template("order/menu.html", view=view, groups=groups.items(), error=error,
                           quantities=quantities, selected_address_id=address_id,
                           voucher_code=voucher_code or ""), status


def _render_quote(q, quantities: dict[int, str], notice: str | None, status: int, payment: str = "COD",
                  notice_kind: str = "notice"):
    return render_template("order/quote.html", quote=q, quantities=quantities, notice=notice,
                           notice_kind=notice_kind, idempotency_token=uuid.uuid4().hex,
                           options=_controller().payment_options(uid()), payment=payment), status


@bp.get("/hubs")
@role_required(Role.CUSTOMER)
def choose_hub():
    return _render_hubs(None)


@bp.get("/hubs/<int:hub_id>")
@role_required(Role.CUSTOMER)
def choose_items(hub_id: int):
    # "Change items" on the quote page links back here with the cart in the query string, so nothing is lost.
    return _render_menu(hub_id, None, _read_quantities(request.args), request.args.get("address_id", type=int),
                        request.args.get("voucher_code", ""), 200)


@bp.post("/quote")
@role_required(Role.CUSTOMER)
def quote():
    hub_id = request.form.get("hub_id", type=int)
    address_id = request.form.get("address_id", type=int)
    voucher_code = request.form.get("voucher_code", "")
    quantities = _read_quantities(request.form)
    try:
        q = _controller().request_quote(uid(), hub_id, address_id, quantities, voucher_code)
    except HubUnavailableError as exc:
        return _render_hubs(str(exc), exc.suggestions, 409)
    except ValidationError as exc:
        if not hub_id:
            return _render_hubs(str(exc), status=400)
        return _render_menu(hub_id, str(exc), quantities, address_id, voucher_code, 400)
    return _render_quote(q, quantities, None, 200)


@bp.post("/confirm")
@role_required(Role.CUSTOMER)
def confirm():
    form = request.form
    hub_id = form.get("hub_id", type=int)
    address_id = form.get("address_id", type=int)
    voucher_code = form.get("voucher_code", "")
    quantities = _read_quantities(form)
    controller = _controller()
    try:
        payment = _read_payment(form)
        if payment.method is PaymentMethod.ONLINE and payment.outcome is None:
            # The online payment goes to the provider (our simulator) first; nothing is saved yet.
            if payment.option not in controller.payment_options(uid()):
                raise ValidationError("This payment option is not offered to your account.")
            return render_template("order/payment_simulator.html", form=form, option=payment.option,
                                   amount=form.get("quoted_total", type=int))
        result = controller.confirm_order(uid(), hub_id, address_id, quantities, form.get("idempotency_token", ""),
                                          form.get("quoted_total", type=int), voucher_code, payment)
    except QuoteChangedError as exc:
        return _render_quote(exc.quote, quantities, str(exc), 409, form.get("payment", "COD"))
    except PaymentDeclinedError as exc:
        return _render_quote(exc.quote, quantities, str(exc), 402, "COD", notice_kind="error")
    except HubUnavailableError as exc:
        return _render_hubs(str(exc), exc.suggestions, 409)
    except ValidationError as exc:
        if not hub_id:
            return _render_hubs(str(exc), status=400)
        return _render_menu(hub_id, str(exc), quantities, address_id, voucher_code, 400)
    return redirect(url_for("order.confirmation", order_id=result.order.id), code=303)


@bp.get("/<int:order_id>/confirmation")
@role_required(Role.CUSTOMER)
def confirmation(order_id: int):
    result = _controller().get_confirmation(uid(), order_id)
    return render_template("order/confirmation.html", result=result)


# ---- SUC-03 / SUC-04 ---------------------------------------------------------------------

@bp.get("/mine")
@role_required(Role.CUSTOMER)
def my_orders():
    return render_template("order/my_orders.html", orders=_tracking().list_my_orders(uid()))


@bp.get("/<int:order_id>")
@role_required(Role.CUSTOMER)
def detail(order_id: int):
    return render_template("order/detail.html", d=_tracking().get_order(uid(), order_id))


@bp.post("/<int:order_id>/replacement")
@role_required(Role.CUSTOMER)
def answer_replacement(order_id: int):
    accept = request.form.get("decision") == "accept"
    offer_id = request.form.get("offer_id", type=int) or 0
    return act(lambda: _tracking().answer_replacement(uid(), order_id, offer_id, accept),
               "Thank you. The kitchen will now confirm your order." if accept
               else "You declined the replacement, so the order will not be cooked. "
                    "An online payment is refunded in full.",
               url_for("order.detail", order_id=order_id))


@bp.post("/<int:order_id>/cancel")
@role_required(Role.CUSTOMER)
def cancel(order_id: int):
    return act(lambda: _tracking().cancel_order(uid(), order_id), f"Order {order_id} is cancelled.",
               url_for("order.detail", order_id=order_id))
