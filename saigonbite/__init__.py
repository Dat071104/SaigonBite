"""SaigonBite online food delivery hub - Iteration 1 increment.

Three layers, four roles:
  presentation/            View        (Flask blueprints, Jinja2 templates)
  business/controllers/    Controller  (one method per system operation in the SSD)
  business/domain/         Domain      (dataclasses and enums, no I/O)
  data_access/             DAO         (sqlite3, hand-written SQL)
"""
import os

from flask import Flask


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True,
                template_folder="presentation/templates",
                static_folder="presentation/static")
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SAIGONBITE_SECRET_KEY", "dev-only-secret-change-me"),
        DATABASE=os.path.join(app.instance_path, "saigonbite.db"),
    )
    if test_config:
        app.config.update(test_config)

    from saigonbite.presentation.main import bp as main_bp
    app.register_blueprint(main_bp)
    return app
