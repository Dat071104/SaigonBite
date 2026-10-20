"""SaigonBite online food delivery hub - Iteration 1 increment.

Three layers, four roles:
  presentation/            View        (Flask blueprints, Jinja2 templates)
  business/controllers/    Controller  (one method per system operation in the SSD)
  business/domain/         Domain      (dataclasses and enums, no I/O)
  data_access/             DAO         (sqlite3, hand-written SQL)
"""
import os

from flask import Flask, render_template


def _vnd(amount: int) -> str:
    return f"{amount:,} VND"


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True,
                template_folder="presentation/templates",
                static_folder="presentation/static")
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SAIGONBITE_SECRET_KEY", "dev-only-secret-change-me"),
        DATABASE=os.environ.get("SAIGONBITE_DATABASE") or os.path.join(app.instance_path, "saigonbite.db"),
    )
    if test_config:
        app.config.update(test_config)

    from saigonbite.business.controllers import AuthorizationError, NotFoundError
    from saigonbite.presentation import auth, db, main, order

    app.teardown_appcontext(db.close_db)
    auth.login_manager.init_app(app)
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(order.bp)
    app.jinja_env.filters["vnd"] = _vnd

    @app.errorhandler(AuthorizationError)
    def _forbidden_business(exc):
        return render_template("error.html", code=403, title="Not allowed", message=str(exc)), 403

    @app.errorhandler(NotFoundError)
    def _not_found_business(exc):
        return render_template("error.html", code=404, title="Not found", message=str(exc)), 404

    @app.errorhandler(403)
    def _forbidden(_exc):
        return render_template("error.html", code=403, title="Not allowed",
                               message="Your account does not have the customer role needed for this page."), 403

    @app.errorhandler(404)
    def _not_found(_exc):
        return render_template("error.html", code=404, title="Not found",
                               message="This page does not exist."), 404

    return app
