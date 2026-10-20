"""UC-01 subset routes: choose hub, items, address -> quote -> confirm -> confirmation.

Routes stay thin: they read the form, call PlaceOrderController and render the result.
"""
import uuid

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user

from saigonbite.business.controllers import PlaceOrderController, QuoteChangedError, ValidationError
from saigonbite.business.domain import Role
from saigonbite.presentation.auth import role_required
from saigonbite.presentation.db import get_db

bp = Blueprint("order", __name__, url_prefix="/order")


def _controller() -> PlaceOrderController:
    return PlaceOrderController(get_db())


def _read_quantities(form) -> dict[int, str]:
    """Collect qty_<menu_item_id> fields. Raw strings: the controller validates them."""
    return {int(k[4:]): v for k, v in form.items() if k.startswith("qty_") and k[4:].isdigit()}


def _render_menu(hub_id: int, error: str | None, quantities: dict[int, str], address_id, status: int):
    try:
        view = _controller().select_hub(current_user.account.id, hub_id)
    except ValidationError as exc:           # unknown or archived hub
        return render_template("order/hubs.html", hubs=_controller().list_hubs(), error=str(exc)), 400
    groups: dict[str, list] = {}                 # brands in menu order, not alphabetical
    for entry in view.menu:
        groups.setdefault(entry.item.brand_name, []).append(entry)
    return render_template("order/menu.html", view=view, groups=groups.items(), error=error,
                           quantities=quantities, selected_address_id=address_id), status


@bp.get("/hubs")
@role_required(Role.CUSTOMER)
def choose_hub():
    return render_template("order/hubs.html", hubs=_controller().list_hubs(), error=None)


@bp.get("/hubs/<int:hub_id>")
@role_required(Role.CUSTOMER)
def choose_items(hub_id: int):
    # "Change items" on the quote page links back here with the cart in the query string, so nothing is lost.
    return _render_menu(hub_id, None, _read_quantities(request.args),
                        request.args.get("address_id", type=int), 200)


@bp.post("/quote")
@role_required(Role.CUSTOMER)
def quote():
    hub_id = request.form.get("hub_id", type=int)
    address_id = request.form.get("address_id", type=int)
    quantities = _read_quantities(request.form)
    try:
        q = _controller().request_quote(current_user.account.id, hub_id, address_id, quantities)
    except ValidationError as exc:
        if not hub_id:
            return render_template("order/hubs.html", hubs=_controller().list_hubs(), error=str(exc)), 400
        return _render_menu(hub_id, str(exc), quantities, address_id, 400)
    return _render_quote(q, quantities, None, 200)


def _render_quote(q, quantities: dict[int, str], notice: str | None, status: int):
    return render_template("order/quote.html", quote=q, quantities=quantities, notice=notice,
                           idempotency_token=uuid.uuid4().hex), status


@bp.post("/confirm")
@role_required(Role.CUSTOMER)
def confirm():
    hub_id = request.form.get("hub_id", type=int)
    address_id = request.form.get("address_id", type=int)
    quantities = _read_quantities(request.form)
    try:
        result = _controller().confirm_order(current_user.account.id, hub_id, address_id, quantities,
                                             request.form.get("idempotency_token", ""),
                                             request.form.get("quoted_total", type=int))
    except QuoteChangedError as exc:
        return _render_quote(exc.quote, quantities, str(exc), 409)
    except ValidationError as exc:
        if not hub_id:
            return render_template("order/hubs.html", hubs=_controller().list_hubs(), error=str(exc)), 400
        return _render_menu(hub_id, str(exc), quantities, address_id, 400)
    return redirect(url_for("order.confirmation", order_id=result.order.id), code=303)


@bp.get("/<int:order_id>/confirmation")
@role_required(Role.CUSTOMER)
def confirmation(order_id: int):
    result = _controller().get_confirmation(current_user.account.id, order_id)
    return render_template("order/confirmation.html", result=result)
