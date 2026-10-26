"""Kitchen staff routes: UC-05 (confirm, reject, offer a replacement), SUC-05 (prepare, ready),
SUC-06 (availability at my hub). Every controller call checks the staff member's hub."""
from flask import Blueprint, render_template, request, url_for

from saigonbite.business.controllers import KitchenController
from saigonbite.business.domain import Role
from saigonbite.presentation.auth import role_required
from saigonbite.presentation.db import get_db
from saigonbite.presentation.helpers import act, uid, boolean_value

bp = Blueprint("kitchen", __name__, url_prefix="/kitchen")


def _controller() -> KitchenController:
    return KitchenController(get_db())


@bp.get("/")
@role_required(Role.KITCHEN_STAFF)
def board():
    return render_template("kitchen/board.html", board=_controller().board(uid()))


@bp.get("/orders/<int:order_id>")
@role_required(Role.KITCHEN_STAFF)
def order(order_id: int):
    return render_template("kitchen/order.html", v=_controller().get_order(uid(), order_id))


@bp.post("/orders/<int:order_id>/confirm")
@role_required(Role.KITCHEN_STAFF)
def confirm(order_id: int):
    return act(lambda: _controller().confirm_order(uid(), order_id), f"Order {order_id} is confirmed.",
               url_for("kitchen.board"))


@bp.post("/orders/<int:order_id>/reject")
@role_required(Role.KITCHEN_STAFF)
def reject(order_id: int):
    return act(lambda: _controller().reject_order(uid(), order_id, request.form.get("reason", "")),
               f"Order {order_id} is rejected and the customer is told why.", url_for("kitchen.order", order_id=order_id))


@bp.post("/orders/<int:order_id>/offer")
@role_required(Role.KITCHEN_STAFF)
def offer(order_id: int):
    line_id, _, item_id = request.form.get("replacement", "").partition(":")
    line_id, item_id = (int(v) if v.isdigit() else 0 for v in (line_id, item_id))
    return act(lambda: _controller().offer_replacement(uid(), order_id, line_id, item_id),
               "The replacement is offered. The order waits for the customer's answer.",
               url_for("kitchen.order", order_id=order_id))


@bp.post("/orders/<int:order_id>/prepare")
@role_required(Role.KITCHEN_STAFF)
def prepare(order_id: int):
    return act(lambda: _controller().start_preparing(uid(), order_id), f"Order {order_id} is being prepared.",
               url_for("kitchen.board"))


@bp.post("/orders/<int:order_id>/ready")
@role_required(Role.KITCHEN_STAFF)
def ready(order_id: int):
    return act(lambda: _controller().mark_ready(uid(), order_id),
               f"Order {order_id} is ready. Shippers can now pick it up.", url_for("kitchen.board"))


@bp.get("/availability")
@role_required(Role.KITCHEN_STAFF)
def availability():
    hub, menu = _controller().list_availability(uid())
    return render_template("kitchen/availability.html", hub=hub, menu=menu)


@bp.post("/availability/<int:item_id>")
@role_required(Role.KITCHEN_STAFF)
def set_availability(item_id: int):
    return act(lambda: _controller().set_availability(uid(), item_id, boolean_value(request.form.get('available',''))),
               "Availability updated.", url_for("kitchen.availability"))
