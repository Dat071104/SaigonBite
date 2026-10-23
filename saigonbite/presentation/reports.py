"""Manager routes: UC-04 Produce management reports (read-only, GET only)."""
from flask import Blueprint, render_template, request

from saigonbite.business.controllers import ReportController, ValidationError
from saigonbite.business.domain import Role
from saigonbite.presentation.auth import role_required
from saigonbite.presentation.db import get_db
from saigonbite.presentation.helpers import uid

bp = Blueprint("reports", __name__, url_prefix="/reports")


def _controller() -> ReportController:
    return ReportController(get_db())


def _filtered(template: str, run):
    args = request.args
    try:
        report = run(args.get("from") or None, args.get("to") or None, args.get("hub", type=int))
    except ValidationError as exc:
        return render_template(template, report=None, error=str(exc), args=args,
                               hubs=_controller().all_hubs()), 400
    return render_template(template, report=report, error=None, args=args, hubs=_controller().all_hubs())


@bp.get("/")
@bp.get("/sales")
@role_required(Role.MANAGER)
def sales():
    return _filtered("reports/sales.html", lambda f, t, h: _controller().sales_report(uid(), f, t, h))


@bp.get("/workload")
@role_required(Role.MANAGER)
def workload():
    return render_template("reports/workload.html", report=_controller().workload_report(uid()))


@bp.get("/delivery")
@role_required(Role.MANAGER)
def delivery():
    return _filtered("reports/delivery.html", lambda f, t, h: _controller().delivery_report(uid(), f, t, h))
