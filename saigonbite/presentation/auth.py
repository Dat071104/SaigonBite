"""Login, logout and server-side role checks (Flask-Login)."""
from functools import wraps
from urllib.parse import urlparse

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user

from saigonbite.business.controllers import AuthController
from saigonbite.business.domain import Role, UserAccount
from saigonbite.presentation.db import get_db

bp = Blueprint("auth", __name__)
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to continue."
login_manager.login_message_category = "info"


class SessionUser(UserMixin):
    """Adapter so the domain UserAccount does not depend on Flask-Login."""

    def __init__(self, account: UserAccount):
        self.account = account

    def get_id(self) -> str:
        return str(self.account.id)

    @property
    def role(self) -> Role:
        return self.account.role

    @property
    def display_name(self) -> str:
        return self.account.display_name


@login_manager.user_loader
def load_user(user_id: str):
    try:
        account = AuthController(get_db()).get_user(int(user_id))
    except ValueError:
        return None
    return SessionUser(account) if account else None


def role_required(*roles: Role):
    """Server-side check: anonymous -> redirect to login; wrong role -> 403."""
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if current_user.role not in roles:
                abort(403)
            return view(*args, **kwargs)
        return wrapped
    return decorator


def _safe_next(target: str | None) -> str | None:
    """Accept only same-site relative paths for the post-login redirect."""
    if target and target.startswith("/") and not target.startswith("//") and not urlparse(target).netloc:
        return target
    return None


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = AuthController(get_db()).authenticate(request.form.get("username", ""),
                                                     request.form.get("password", ""))
        if user is None:
            return render_template("login.html", error="Wrong username or password.",
                                   username=request.form.get("username", ""),
                                   next=request.form.get("next", "")), 401
        login_user(SessionUser(user))
        default = url_for("order.choose_hub") if user.role is Role.CUSTOMER else url_for("main.home")
        return redirect(_safe_next(request.form.get("next")) or default)
    return render_template("login.html", error=None, username="", next=request.args.get("next", ""))


@bp.post("/logout")
def logout():
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for("main.home"))
