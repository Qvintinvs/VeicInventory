import app_container
from dotenv import load_dotenv
from flask import Flask


def request_method_error(error: Exception):
    return str(error), 405


def main():
    could_load_dotenv = load_dotenv()

    if not could_load_dotenv:
        raise Exception("Missing Dotenv")

    container = app_container.InventoryAppContainer()

    main_page = container.main_page()

    main_blueprint = main_page.add_to()

    app = Flask(__name__)

    app.register_blueprint(main_blueprint)

    app.register_error_handler(405, request_method_error)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance/app.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db = container.database()

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.run()


if __name__ == "__main__":
    main()
