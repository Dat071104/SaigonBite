"""Admin routes: UC-03 hubs and capacity, UC-06 brands, menu items and hub menus,
SUC-07 vouchers, SUC-08 user accounts, SUC-09 archive closed orders."""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from saigonbite.business.controllers import (STAFF_ROLES, HubController, MenuController, OrderArchiveController,
                                             UserAdminController, ValidationError, VoucherController)
from saigonbite.business.domain import DiscountType, Role
from saigonbite.presentation.auth import role_required
from saigonbite.presentation.db import get_db
from saigonbite.presentation.helpers import act, uid, boolean_value

bp = Blueprint("admin", __name__, url_prefix="/admin")


def _form_page(template: str, save, success: str, back: str, **context):
    """GET shows the form; POST saves it, or shows it again with the error and the entered values."""
    if request.method == "POST":
        try:
            save()
        except ValidationError as exc:
            return render_template(template, error=str(exc), form=request.form, **context), 400
        flash(success, "success")
        return redirect(back, code=303)
    return render_template(template, error=None, form=None, **context)


# ---- UC-03 hubs ----------------------------------------------------------------------------

def _hubs() -> HubController:
    return HubController(get_db())


@bp.get("/")
@bp.get("/hubs")
@role_required(Role.ADMIN)
def hubs():
    include_archived = request.args.get('includeArchived', 'true').lower() not in ('0', 'false')
    return render_template("admin/hubs.html", hubs=_hubs().list_hubs(uid(), include_archived))


@bp.route("/hubs/new", methods=["GET", "POST"])
@role_required(Role.ADMIN)
def new_hub():
    return _form_page("admin/hub_form.html", lambda: _hubs().create_hub(uid(), request.form),
                      "The hub is created. Add dishes to its menu before it can take orders.",
                      url_for("admin.hubs"), view=None)


@bp.route("/hubs/<int:hub_id>", methods=["GET", "POST"])
@role_required(Role.ADMIN)
def edit_hub(hub_id: int):
    view = _hubs().get_hub(uid(), hub_id)
    return _form_page("admin/hub_form.html", lambda: _hubs().update_hub(uid(), hub_id, request.form),
                      "The hub is saved.", url_for("admin.hubs"), view=view)


@bp.post("/hubs/<int:hub_id>/archive")
@role_required(Role.ADMIN)
def archive_hub(hub_id: int):
    return act(lambda: _hubs().archive_hub(uid(), hub_id),
               "The hub is archived. It no longer takes orders; its history is kept.", url_for("admin.hubs"))


# ---- UC-06 brands, menu items, hub menus ----------------------------------------------------

def _menu() -> MenuController:
    return MenuController(get_db())


@bp.get("/menu")
@role_required(Role.ADMIN)
def catalogue():
    view = _menu().list_catalogue(uid())
    return render_template("admin/catalogue.html", c=view['catalogue'], hubs=view['hubs'])


@bp.post("/brands")
@role_required(Role.ADMIN)
def create_brand():
    return act(lambda: _menu().create_brand(uid(), request.form.get("name", "")), "The brand is created.",
               url_for("admin.catalogue"))


@bp.post("/brands/<int:brand_id>")
@role_required(Role.ADMIN)
def rename_brand(brand_id: int):
    return act(lambda: _menu().rename_brand(uid(), brand_id, request.form.get("name", "")), "The brand is renamed.",
               url_for("admin.catalogue"))


@bp.post("/brands/<int:brand_id>/archive")
@role_required(Role.ADMIN)
def archive_brand(brand_id: int):
    return act(lambda: _menu().archive_brand(uid(), brand_id),
               "The brand is archived. Its dishes can no longer be ordered.", url_for("admin.catalogue"))


@bp.route("/items/new", methods=["GET", "POST"])
@role_required(Role.ADMIN)
def new_item():
    return _form_page("admin/item_form.html", lambda: _menu().create_item(uid(), request.form),
                      "The dish is created. List it at a hub so customers can order it.",
                      url_for("admin.catalogue"), item=None, brands=_menu().catalogue(uid()).brands)


@bp.route("/items/<int:item_id>", methods=["GET", "POST"])
@role_required(Role.ADMIN)
def edit_item(item_id: int):
    catalogue = _menu().catalogue(uid())
    item = next((i for i in catalogue.items if i.id == item_id), None)
    if item is None:
        return render_template("error.html", code=404, title="Not found", message="Dish not found."), 404
    return _form_page("admin/item_form.html", lambda: _menu().update_item(uid(), item_id, request.form),
                      "The dish is saved. Orders already placed keep their old name and price.",
                      url_for("admin.catalogue"), item=item, brands=catalogue.brands)


@bp.post("/items/<int:item_id>/archive")
@role_required(Role.ADMIN)
def archive_item(item_id: int):
    return act(lambda: _menu().archive_item(uid(), item_id),
               "The dish is archived. It can no longer be ordered.", url_for("admin.catalogue"))


@bp.get("/hubs/<int:hub_id>/menu")
@role_required(Role.ADMIN)
def hub_menu(hub_id: int):
    return render_template("admin/hub_menu.html", m=_menu().list_catalogue(uid(), hub_id)['hub_menu'])


@bp.post("/hubs/<int:hub_id>/menu")
@role_required(Role.ADMIN)
def list_item(hub_id: int):
    item_id = request.form.get("item_id", type=int) or 0
    return act(lambda: _menu().list_item_at_hub(uid(), hub_id, item_id,boolean_value(request.form.get('available','1'))), "The dish is on the hub's menu.",
               url_for("admin.hub_menu", hub_id=hub_id))


@bp.post("/hubs/<int:hub_id>/menu/<int:item_id>/remove")
@role_required(Role.ADMIN)
def unlist_item(hub_id: int, item_id: int):
    return act(lambda: _menu().unlist_item_at_hub(uid(), hub_id, item_id), "The dish is off the hub's menu.",
               url_for("admin.hub_menu", hub_id=hub_id))


@bp.post("/hubs/<int:hub_id>/menu/<int:item_id>/availability")
@role_required(Role.ADMIN)
def hub_item_availability(hub_id: int, item_id: int):
    return act(lambda: _menu().set_availability(uid(), hub_id, item_id, boolean_value(request.form.get('available',''))), "Availability updated.",
               url_for("admin.hub_menu", hub_id=hub_id))


# ---- SUC-07 vouchers ----------------------------------------------------------------------

def _vouchers() -> VoucherController:
    return VoucherController(get_db())


@bp.get("/vouchers")
@role_required(Role.ADMIN)
def vouchers():
    return render_template("admin/vouchers.html", vouchers=_vouchers().list_vouchers(uid()))


@bp.route("/vouchers/new", methods=["GET", "POST"])
@role_required(Role.ADMIN)
def new_voucher():
    return _form_page("admin/voucher_form.html", lambda: _vouchers().create_voucher(uid(), request.form),
                      "The voucher is created.", url_for("admin.vouchers"), voucher=None, types=list(DiscountType))


@bp.route("/vouchers/<int:voucher_id>", methods=["GET", "POST"])
@role_required(Role.ADMIN)
def edit_voucher(voucher_id: int):
    voucher = _vouchers().get_voucher(uid(), voucher_id)
    return _form_page("admin/voucher_form.html", lambda: _vouchers().update_voucher(uid(), voucher_id, request.form),
                      "The voucher is saved. Orders that used it keep their discount.", url_for("admin.vouchers"),
                      voucher=voucher, types=list(DiscountType))


@bp.post("/vouchers/<int:voucher_id>/archive")
@role_required(Role.ADMIN)
def archive_voucher(voucher_id: int):
    return act(lambda: _vouchers().archive_voucher(uid(), voucher_id),
               "The voucher is archived and can no longer be used.", url_for("admin.vouchers"))


# ---- SUC-08 user accounts -------------------------------------------------------------------

def _users() -> UserAdminController:
    return UserAdminController(get_db())


@bp.get("/users")
@role_required(Role.ADMIN)
def users():
    return render_template("admin/users.html", users=_users().list_users(uid()))


@bp.route("/users/new", methods=["GET", "POST"])
@role_required(Role.ADMIN)
def new_user():
    return _form_page("admin/user_form.html", lambda: _users().create_staff(uid(), request.form),
                      "The account is created.", url_for("admin.users"), user=None, roles=STAFF_ROLES,
                      hubs=_users().hubs_for_staff(), customer=None)


@bp.route("/users/<int:user_id>", methods=["GET", "POST"])
@role_required(Role.ADMIN)
def edit_user(user_id: int):
    user = _users().get_user(uid(), user_id)
    return _form_page("admin/user_form.html", lambda: _users().update_user(uid(), user_id, request.form),
                      "The account is saved.", url_for("admin.users"), user=user, roles=STAFF_ROLES,
                      hubs=_users().hubs_for_staff(), customer=_users().get_customer(uid(), user_id))


@bp.post("/users/<int:user_id>/active")
@role_required(Role.ADMIN)
def set_user_active(user_id: int):
    return act(lambda: _users().set_active(uid(), user_id, boolean_value(request.form.get('active',''))),
               "Account activation updated.",
               url_for("admin.users"))


# ---- SUC-09 archive closed orders ---------------------------------------------------------

def _archive() -> OrderArchiveController:
    return OrderArchiveController(get_db())


@bp.post('/archive/<int:order_id>')
@role_required(Role.ADMIN)
def archive_order(order_id: int):
    return act(lambda: _archive().archive_order(uid(), order_id),
               'The closed order is archived. Its history and reports are kept.', url_for('admin.archive'))


@bp.get('/archive/<int:order_id>')
@role_required(Role.ADMIN)
def archived_history(order_id: int):
    return render_template('admin/archived_history.html', **_archive().archived_history(uid(), order_id))


@bp.get("/archive")
@role_required(Role.ADMIN)
def archive():
    day = request.args.get("closed_before", "")
    preview, error = None, None
    if day:
        try:
            preview = _archive().preview(uid(), day)
        except ValidationError as exc:
            error = str(exc)
    return render_template("admin/archive.html", preview=preview, error=error, day=day,
                           archived=_archive().list_archived(uid()))


@bp.post("/archive")
@role_required(Role.ADMIN)
def archive_orders():
    day = request.form.get("closed_before", "")
    try:
        n = _archive().archive(uid(), day)
    except ValidationError as exc:
        flash(str(exc), "error")
    else:
        flash(f"{n} finished order(s) archived. Reports still include them.", "success")
    return redirect(url_for("admin.archive"), code=303)
