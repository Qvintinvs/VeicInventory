import database_setup
from app_config import AppConfig
from dotenv import load_dotenv
from flask import Flask
from flask_wtf import CSRFProtect
from inventory_app_container import InventoryAppContainer
from routes import (
    netcdf_api_routes,
    round_processing_routes,
    vehicular_inventory_routes,
)


def request_method_error(error: Exception):
    return str(error), 405


def load_configuration():
    could_load_dotenv = load_dotenv()

    if not could_load_dotenv:
        raise Exception("Missing dotenv file")


def initialize_app_container(app: Flask):
    container = InventoryAppContainer()

    config = container.config

    config.namelist_remote_path.from_env("NAMELIST_REMOTE_PATH", required=True)

    config.hostname.from_env("SSH_HOST", required=True)
    config.username.from_env("SSH_NAME", required=True)
    config.password.from_env("SSH_PASS")

    config.from_dict(app.config)

    return container


def register_app_routes(app: Flask):
    csrf = CSRFProtect(app)

    inventory_blueprint = (
        vehicular_inventory_routes.create_vehicular_inventory_blueprint()
    )

    netcdf_api_blueprint = netcdf_api_routes.create_netcdf_api_blueprint()

    processing_blueprint = round_processing_routes.create_round_processing_blueprint()

    csrf.exempt(netcdf_api_blueprint)

    app.register_blueprint(inventory_blueprint)
    app.register_blueprint(processing_blueprint)

    app.register_blueprint(netcdf_api_blueprint)

    app.register_error_handler(405, request_method_error)


def create_app():
    load_configuration()

    app = Flask(__name__)

    app.config.from_object(AppConfig)

    container = initialize_app_container(app)

    container.wire(
        modules=(
            database_setup,
            vehicular_inventory_routes,
            round_processing_routes,
            netcdf_api_routes,
        )
    )

    return app


def main():
    app = create_app()

    register_app_routes(app)

    database_setup.setup_database_within(app)

    app.run()


if __name__ == "__main__":
    main()
