"""SaigonBite online food delivery hub - Part 2 build (six main use cases and their support).

Three layers, four roles:
  presentation/            View        (Flask blueprints, Jinja2 templates, CSRF)
  business/controllers/    Controller  (one class per use case, one method per system operation in the SSD)
  business/domain/         Domain      (dataclasses, enums, state machines, pricing rules; no I/O)
  data_access/             DAO         (sqlite3, hand-written SQL; payment simulator)
"""
import logging
import os

from flask import Flask, render_template

NAV = {
    "CUSTOMER": [("order.choose_hub", "Order food"), ("order.my_orders", "My orders"), ("account.profile", "Profile")],
    "KITCHEN_STAFF": [("kitchen.board", "Kitchen board"), ("kitchen.availability", "Availability")],
    "SHIPPER": [("delivery.board", "Deliveries")],
    "ADMIN": [("admin.hubs", "Hubs"), ("admin.catalogue", "Brands and menu"), ("admin.vouchers", "Vouchers"),
              ("admin.users", "Users"), ("admin.archive", "Archive orders")],
    "MANAGER": [("reports.sales", "Sales"), ("reports.workload", "Workload"), ("reports.delivery", "Delivery")],
}


def _vnd(amount: int) -> str:
    return f"{amount:,} VND"


def _vn_time(iso_utc: str) -> str:
    """Show a stored UTC timestamp in Ho Chi Minh City time (UTC+7), e.g. 12:05, 20/10/2026."""
    from datetime import datetime, timedelta, timezone
    try:
        moment = datetime.fromisoformat(iso_utc)
    except (TypeError, ValueError):
        return iso_utc or ""
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    return moment.astimezone(timezone(timedelta(hours=7))).strftime("%H:%M, %d/%m/%Y")


def _label(value) -> str:
    """OUT_FOR_DELIVERY -> Out for delivery (enum values shown to people)."""
    text = getattr(value, "value", value) or ""
    return text.replace("_", " ").lower().capitalize()


def _production_config(app: Flask) -> None:
    """SAIGONBITE_ENV=production: a real secret is required, cookies are secure, the proxy is trusted."""
    from werkzeug.middleware.proxy_fix import ProxyFix
    secret = os.environ.get("SAIGONBITE_SECRET_KEY", "")
    if len(secret) < 32 or secret == "dev-only-secret-change-me":
        raise RuntimeError("SAIGONBITE_SECRET_KEY must be set to a random value of at least 32 characters "
                           "when SAIGONBITE_ENV=production.")
    https = os.environ.get("SAIGONBITE_HTTPS", "1") == "1"
    app.config.update(SECRET_KEY=secret, SESSION_COOKIE_SECURE=https, REMEMBER_COOKIE_SECURE=https,
                      SESSION_COOKIE_SAMESITE="Lax", DEBUG=False)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True,
                template_folder="presentation/templates",
                static_folder="presentation/static")
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SAIGONBITE_SECRET_KEY", "dev-only-secret-change-me"),
        DATABASE=os.environ.get("SAIGONBITE_DATABASE") or os.path.join(app.instance_path, "saigonbite.db"),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        CSRF_ENABLED=True,
    )
    if os.environ.get("SAIGONBITE_ENV") == "production":
        _production_config(app)
    if test_config:
        app.config.update(test_config)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    from saigonbite.business.controllers import AuthorizationError, ConflictError, NotFoundError
    from saigonbite.presentation import (account, admin, auth, db, delivery, kitchen, main, order, reports,
                                         security)

    app.teardown_appcontext(db.close_db)
    auth.login_manager.init_app(app)
    security.init_csrf(app)
    for module in (main, auth, order, account, kitchen, delivery, admin, reports):
        app.register_blueprint(module.bp)
    app.jinja_env.filters["vnd"] = _vnd
    app.jinja_env.filters["vn_time"] = _vn_time
    app.jinja_env.filters["label"] = _label

    @app.context_processor
    def _navigation():
        from flask_login import current_user
        links = NAV.get(current_user.role.value, []) if current_user.is_authenticated else []
        return {"nav_links": links}

    def _page(code: int, title: str, message: str):
        return render_template("error.html", code=code, title=title, message=message), code

    @app.errorhandler(AuthorizationError)
    def _forbidden_business(exc):
        return _page(403, "Not allowed", str(exc))

    @app.errorhandler(NotFoundError)
    def _not_found_business(exc):
        return _page(404, "Not found", str(exc))

    @app.errorhandler(ConflictError)
    def _conflict(exc):
        return _page(409, "Already changed", str(exc))

    @app.errorhandler(400)
    def _bad_request(exc):
        if getattr(exc, "description", "") == "csrf":
            return _page(400, "Form expired", "This form has expired or did not come from SaigonBite. "
                                              "Go back, reload the page and try again.")
        return _page(400, "Bad request", "The request could not be understood.")

    @app.errorhandler(403)
    def _forbidden(_exc):
        return _page(403, "Not allowed", "Your account does not have the role needed for this page.")

    @app.errorhandler(404)
    def _not_found(_exc):
        return _page(404, "Not found", "This page does not exist.")

    @app.errorhandler(405)
    def _method_not_allowed(_exc):
        return _page(405, "Page expired", "This page only opens from a form. Go back and start again.")

    return app
