from dependency_injector import containers, providers
from flask_sqlalchemy import SQLAlchemy
from models.base import Base
from services.namelist_server_sending import connection_settings, wrf_service
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

    wrf_service = providers.Singleton(
        wrf_service.SSHWRFService,
        settings=connection_settings,
        namelist_remote_path=config.namelist_remote_path,
    )
