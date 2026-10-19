"""Entry point for `flask run` (Flask finds `app.py` and the `app` object)."""
from saigonbite import create_app

app = create_app()
