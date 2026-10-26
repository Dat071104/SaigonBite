"""SUC-02: register (local or tourist), edit the profile, manage delivery addresses."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user

from saigonbite.business.controllers import AccountController, NotFoundError, ValidationError
from saigonbite.business.controllers.presentation_contract import Role, district_choices
from saigonbite.presentation.auth import SessionUser, role_required
from saigonbite.presentation.db import get_db
from saigonbite.presentation.helpers import act, uid

bp = Blueprint("account", __name__)
DISTRICTS = district_choices()


def _controller() -> AccountController:
    return AccountController(get_db())


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    if request.method == "POST":
        try:
            user = _controller().register(request.form)
        except ValidationError as exc:
            return render_template("account/register.html", error=str(exc), form=request.form), 400
        login_user(SessionUser(user))
        flash("Welcome to SaigonBite. Add a delivery address to start ordering.", "success")
        return redirect(url_for("account.new_address"), code=303)
    return render_template("account/register.html", error=None, form={})


@bp.get("/account")
@role_required(Role.CUSTOMER)
def profile():
    return render_template("account/profile.html", p=_controller().get_profile(uid()), error=None, form=None)


@bp.post("/account")
@role_required(Role.CUSTOMER)
def update_profile():
    try:
        _controller().update_profile(uid(), request.form)
    except ValidationError as exc:
        return render_template("account/profile.html", p=_controller().get_profile(uid()), error=str(exc),
                               form=request.form), 400
    flash("Your profile is saved.", "success")
    return redirect(url_for("account.profile"), code=303)


@bp.route("/account/addresses/new", methods=["GET", "POST"])
@role_required(Role.CUSTOMER)
def new_address():
    if request.method == "POST":
        try:
            _controller().add_address(uid(), request.form)
        except ValidationError as exc:
            return render_template("account/address.html", address=None, error=str(exc), form=request.form,
                                   districts=DISTRICTS), 400
        flash("The address is saved.", "success")
        return redirect(url_for("account.profile"), code=303)
    return render_template("account/address.html", address=None, error=None, form={}, districts=DISTRICTS)


@bp.route("/account/addresses/<int:address_id>", methods=["GET", "POST"])
@role_required(Role.CUSTOMER)
def edit_address(address_id: int):
    profile = _controller().get_profile(uid())
    address = next((a for a in profile.addresses if a.id == address_id), None)
    if address is None:
        raise NotFoundError("Address not found.")
    if request.method == "POST":
        try:
            _controller().update_address(uid(), address_id, request.form)
        except ValidationError as exc:
            return render_template("account/address.html", address=address, error=str(exc), form=request.form,
                                   districts=DISTRICTS), 400
        flash("The address is saved. Orders already placed keep the old address.", "success")
        return redirect(url_for("account.profile"), code=303)
    return render_template("account/address.html", address=address, error=None, form=None,
                           districts=DISTRICTS)


@bp.post("/account/addresses/<int:address_id>/archive")
@role_required(Role.CUSTOMER)
def archive_address(address_id: int):
    return act(lambda: _controller().archive_address(uid(), address_id),
               "The address is removed from your list. Past orders keep it.", url_for("account.profile"))
