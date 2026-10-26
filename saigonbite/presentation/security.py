"""CSRF protection for every state-changing form (plan §2.4).

One random token per session; every POST must send it back in the csrf_token field. This is separate
from the checkout's idempotency token, which stops a double submit, not a forged request.
Tests send explicit session-bound tokens; protection stays enabled.
"""
import hmac
import secrets

from flask import Flask, abort, current_app, request, session

FIELD = "csrf_token"


def csrf_token() -> str:
    if FIELD not in session:
        session[FIELD] = secrets.token_urlsafe(32)
    return session[FIELD]


def init_csrf(app: Flask) -> None:
    app.jinja_env.globals["csrf_token"] = csrf_token

    @app.before_request
    def _check_csrf():
        if request.method not in ("POST", "PUT", "PATCH", "DELETE"):
            return None
        expected = session.get(FIELD)
        sent = request.form.get(FIELD, "")
        if not expected or not hmac.compare_digest(expected.encode('utf-8'), sent.encode('utf-8')):
            abort(400, description="csrf")
        return None
