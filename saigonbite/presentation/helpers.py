"""Small helpers shared by the blueprints."""
from typing import Callable

from flask import flash, redirect
from flask_login import current_user

from saigonbite.business.controllers import ConflictError, ValidationError


def uid() -> int:
    return current_user.account.id


def act(action: Callable[[], object], success: str, back: str):
    """Post/redirect/get for a button: run the controller method, flash the outcome, go back.

    A broken rule (ValidationError) or a state that changed meanwhile (ConflictError) becomes an error
    message on the same screen; nothing was written in either case. Authorization and not-found errors
    go to the error pages.
    """
    try:
        action()
    except (ValidationError, ConflictError) as exc:
        flash(str(exc), "error")
    else:
        flash(success, "success")
    return redirect(back, code=303)
