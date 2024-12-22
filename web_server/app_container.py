from dependency_injector import containers, providers
from flask_sqlalchemy import SQLAlchemy
from models import vasques_vehicle_model, vehicles_database


class InventoryAppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    vehicular_inventory = providers.Singleton(
        vehicles_database.VehiclesDatabase,
        db=SQLAlchemy(model_class=vasques_vehicle_model.Base),
    )
