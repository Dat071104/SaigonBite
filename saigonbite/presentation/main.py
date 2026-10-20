"""Home page blueprint (public)."""
from flask import Blueprint, redirect, render_template, url_for

bp = Blueprint("main", __name__)


@bp.get("/")
def home():
    return render_template("home.html")


@bp.get("/favicon.ico")
def favicon():
    """Browsers and audit tools ask for /favicon.ico even when the page names its icon."""
    return redirect(url_for("static", filename="favicon.svg"), 301)
