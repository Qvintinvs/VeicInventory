import app_container
from dotenv import load_dotenv
from flask import Flask
from views.index_view import IndexView


def request_method_error(error: Exception):
    return str(error), 405


def main():
    could_load_dotenv = load_dotenv()

    if not could_load_dotenv:
        raise Exception("Missing Dotenv")

    container = app_container.InventoryAppContainer()

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    inventory = container.vehicular_inventory()

    inventory.initialize_database_in(app)

    main_page = IndexView(inventory)

    main_blueprint = main_page.add_to()

    app.register_blueprint(main_blueprint)

    app.register_error_handler(405, request_method_error)

    app.run()


if __name__ == "__main__":
    main()
