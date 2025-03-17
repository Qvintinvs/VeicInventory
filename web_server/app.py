from secrets import token_hex

from app_container import InventoryAppContainer
from dotenv import load_dotenv
from flask import Flask
from flask_wtf import CSRFProtect
from views.vehicular_inventory_view import VehicularInventoryView


def request_method_error(error: Exception):
    return str(error), 405


def main():
    could_load_dotenv = load_dotenv()

    if not could_load_dotenv:
        raise Exception("Missing Dotenv")

    container = InventoryAppContainer()

    config = container.config

    config.namelist_remote_path.from_env("NAMELIST_REMOTE_PATH", required=True)

    config.hostname.from_env("SSH_HOST", required=True)
    config.username.from_env("SSH_NAME", required=True)
    config.password.from_env("SSH_PASS")

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.secret_key = token_hex(16)

    _ = CSRFProtect(app)

    inventory = container.vehicular_inventory()

    inventory.initialize_database_in(app)

    main_page = VehicularInventoryView(inventory)

    main_blueprint = main_page.setup_routes()

    app.register_blueprint(main_blueprint)

    app.register_error_handler(405, request_method_error)

    app.run()


if __name__ == "__main__":
    main()
