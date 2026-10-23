"""Shipper routes: UC-02 Deliver an order (pick up, deliver and collect cash, or report a failure)."""
from flask import Blueprint, render_template, request, url_for

from saigonbite.business.controllers import DeliveryController
from saigonbite.business.domain import Role
from saigonbite.presentation.auth import role_required
from saigonbite.presentation.db import get_db
from saigonbite.presentation.helpers import act, uid

bp = Blueprint("delivery", __name__, url_prefix="/delivery")


def _controller() -> DeliveryController:
    return DeliveryController(get_db())


@bp.get("/")
@role_required(Role.SHIPPER)
def board():
    return render_template("delivery/board.html", board=_controller().board(uid()))


@bp.get("/orders/<int:order_id>")
@role_required(Role.SHIPPER)
def detail(order_id: int):
    return render_template("delivery/detail.html", v=_controller().get_delivery(uid(), order_id))


@bp.post("/orders/<int:order_id>/pickup")
@role_required(Role.SHIPPER)
def pick_up(order_id: int):
    return act(lambda: _controller().pick_up(uid(), order_id), f"You picked up order {order_id}.",
               url_for("delivery.detail", order_id=order_id))


@bp.post("/orders/<int:order_id>/delivered")
@role_required(Role.SHIPPER)
def delivered(order_id: int):
    return act(lambda: _controller().confirm_delivered(uid(), order_id, request.form.get("cash_collected")),
               f"Order {order_id} is delivered.", url_for("delivery.detail", order_id=order_id))


@bp.post("/orders/<int:order_id>/failed")
@role_required(Role.SHIPPER)
def failed(order_id: int):
    return act(lambda: _controller().report_failure(uid(), order_id, request.form.get("reason", "")),
               f"The failed delivery of order {order_id} is recorded. Bring the food back to the hub.",
               url_for("delivery.detail", order_id=order_id))
