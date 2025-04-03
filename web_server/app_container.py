from multiprocessing import Queue

from dependency_injector import containers, providers
from flask_sqlalchemy import SQLAlchemy
from models.base import Base
from services import (
    connection_settings,
    ssh_wrf_service,
    vasques_emission_repository,
    wrf_rounds_queue_worker,
    wrf_rounds_repository,
)


class InventoryAppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    sql_db = providers.Singleton(SQLAlchemy, model_class=Base)

    vasques_emission_repository = providers.Singleton(
        vasques_emission_repository.VasquesEmissionRepository, sql_db=sql_db
    )

    wrf_rounds_repository = providers.Singleton(
        wrf_rounds_repository.WRFRoundsRepository, sql_db=sql_db
    )

    connection_settings = providers.Singleton(
        connection_settings.ConnectionSettings,
        hostname=config.hostname,
        username=config.username,
        password=config.password,
    )

    wrf_service = providers.Singleton(
        ssh_wrf_service.SSHWRFService,
        settings=connection_settings,
        namelist_remote_path=config.namelist_remote_path,
    )

    rounds_queue = providers.Singleton(Queue)

    wrf_rounds_queue_worker = providers.Singleton(
        wrf_rounds_queue_worker.WRFRoundsQueueWorker, rounds_queue, wrf_service
    )
