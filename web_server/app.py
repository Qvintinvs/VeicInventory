import database_setup
from app_config import AppConfig
from dotenv import load_dotenv
from flask import Flask
from flask_wtf import CSRFProtect
from inventory_app_container import InventoryAppContainer
from routes import (
    round_processing_routes,
    vehicular_inventory_routes,
    wrf_round_api_routes,
)


def request_method_error(error: Exception):
    return str(error), 405


def load_configuration():
    could_load_dotenv = load_dotenv()

    if not could_load_dotenv:
        raise Exception("Missing dotenv file")


def initialize_container_within(app_instance: Flask):
    container = InventoryAppContainer()

    config = container.config

    config.namelist_remote_path.from_env("NAMELIST_REMOTE_PATH", required=True)

    config.hostname.from_env("SSH_HOST", required=True)
    config.username.from_env("SSH_NAME", required=True)
    config.password.from_env("SSH_PASS")

    config.from_dict(app_instance.config)

    return container


def register_routes_of(app: Flask):
    csrf = CSRFProtect(app)

    inventory_routes = vehicular_inventory_routes.register_vehicular_inventory_routes()

    api_routes = wrf_round_api_routes.register_wrf_round_api_routes()

    processing_routes = round_processing_routes.register_round_processing_routes()

    csrf.exempt(api_routes)

    app.register_blueprint(inventory_routes)
    app.register_blueprint(api_routes)
    app.register_blueprint(processing_routes)

    app.register_error_handler(405, request_method_error)


def create_app():
    load_configuration()

    app = Flask(__name__)

    app.config.from_object(AppConfig)

    container = initialize_container_within(app)

    container.wire(
        modules=(
            vehicular_inventory_routes,
            wrf_round_api_routes,
            round_processing_routes,
            database_setup,
        )
    )

    worker = container.wrf_rounds_queue_worker()
    worker.start()

    return app


def main():
    app = create_app()

    register_routes_of(app)

    database_setup.setup_database_within(app)

    app.run()


if __name__ == "__main__":
    main()
