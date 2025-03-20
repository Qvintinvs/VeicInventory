from dependency_injector import containers, providers
from flask_sqlalchemy import SQLAlchemy
from models.base import Base
from services import (
    connection_settings,
    vehicles_repository,
    wrf_service,
    wrf_rounds_repository,
)


class InventoryAppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    sql_db = providers.Singleton(SQLAlchemy, model_class=Base)

    vehicular_inventory = providers.Singleton(
        vehicles_repository.VehiclesRepository, sql_db=sql_db
    )

    wrf_rounds_db = providers.Singleton(
        wrf_rounds_repository.WRFRoundsRepository, sql_db=sql_db
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
