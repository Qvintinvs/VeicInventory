from app_config import AppConfig
from app_container import InventoryAppContainer
from dotenv import load_dotenv
from flask import Flask
from flask_wtf import CSRFProtect
from routes import vehicular_inventory_routes, wrf_rounds_api_routes


def request_method_error(error: Exception):
    return str(error), 405


def load_configuration():
    could_load_dotenv = load_dotenv()

    if not could_load_dotenv:
        raise Exception("Missing dotenv file")


def initialize_flask_app():
    app = Flask(__name__)

    app.config.from_object(AppConfig)

    return app


def initialize_container_within(app_instance: Flask):
    container = InventoryAppContainer()

    config = container.config

    config.namelist_remote_path.from_env("NAMELIST_REMOTE_PATH", required=True)

    config.hostname.from_env("SSH_HOST", required=True)
    config.username.from_env("SSH_NAME", required=True)
    config.password.from_env("SSH_PASS")

    config.from_dict(app_instance.config)

    main_db = container.sql_db()

    main_db.init_app(app_instance)

    with app_instance.app_context():
        main_db.create_all()

    return container


app = initialize_flask_app()

csrf = CSRFProtect(app)


def main():
    load_configuration()

    container = initialize_container_within(app)

    container.wire(modules=(vehicular_inventory_routes, wrf_rounds_api_routes))

    worker = container.wrf_rounds_queue_worker()
    worker.start()

    inventory_routes = vehicular_inventory_routes.register_vehicular_inventory_routes()

    api_routes = wrf_rounds_api_routes.register_wrf_rounds_api_routes()

    csrf.exempt(api_routes)

    app.register_blueprint(inventory_routes)
    app.register_blueprint(api_routes, url_prefix="/wrf_rounds_api")

    app.register_error_handler(405, request_method_error)

    app.run()


if __name__ == "__main__":
    main()
