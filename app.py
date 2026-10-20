"""Entry point for `flask run`, Docker and Vercel (all three find the `app` object here).

On Vercel only /tmp is writable, so the database lives there and is created and seeded on a cold
start. It is a demo database: it resets when the function restarts, and each running instance
has its own copy.
"""
import os

if os.environ.get("VERCEL") and not os.environ.get("SAIGONBITE_DATABASE"):
    os.environ["SAIGONBITE_DATABASE"] = "/tmp/saigonbite.db"

from saigonbite import create_app  # noqa: E402

app = create_app()

if os.environ.get("VERCEL") and not os.path.exists(app.config["DATABASE"]):
    from init_db import build_database
    build_database(app.config["DATABASE"])
