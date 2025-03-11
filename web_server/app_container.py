from dependency_injector import containers, providers
from flask_sqlalchemy import SQLAlchemy
from models.base import Base
from services.namelist_server_sending import connection_settings
from services.vehicles_repository import VehiclesRepository


class InventoryAppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    vehicular_inventory = providers.Singleton(
        VehiclesRepository, sql_db=SQLAlchemy(model_class=Base)
    )

    connection_settings = providers.Singleton(
        connection_settings.ConnectionSettings,
        hostname=config.hostname,
        username=config.username,
        password=config.password,
    )
