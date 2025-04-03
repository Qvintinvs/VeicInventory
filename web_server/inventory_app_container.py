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
        vasques_emission_repository.VasquesEmissionRepository, sql_db
    )

    wrf_round_repository = providers.Singleton(
        wrf_rounds_repository.WRFRoundRepository, sql_db
    )

    remote_wrf_server_connection_settings = providers.Singleton(
        connection_settings.WRFRemoteConnectionSettings,
        config.hostname,
        config.username,
        config.password,
    )

    ssh_round_namelist_sender = providers.Singleton(
        ssh_wrf_service.SSHRoundNamelistSender,
        remote_wrf_server_connection_settings,
        config.namelist_remote_path,
    )

    rounds_queue = providers.Singleton(Queue)

    wrf_rounds_queue_worker = providers.Singleton(
        wrf_rounds_queue_worker.WRFRoundProcessor,
        rounds_queue,
        ssh_round_namelist_sender,
    )
