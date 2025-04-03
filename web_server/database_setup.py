from dependency_injector.wiring import Provide, inject
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from inventory_app_container import InventoryAppContainer


@inject
def setup_database_within(
    app_instance: Flask,
    main_db: SQLAlchemy = Provide[InventoryAppContainer.sql_db],
):
    main_db.init_app(app_instance)

    with app_instance.app_context():
        main_db.create_all()
