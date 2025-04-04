from multiprocessing import Queue

from dependency_injector import containers, providers
from flask_sqlalchemy import SQLAlchemy
from models.base import Base
from services import (
    ssh_round_namelist_sender,
    vasques_emission_repository,
    wrf_remote_connection_settings,
    wrf_round_processor,
    wrf_round_repository,
)


class InventoryAppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    sql_db = providers.Singleton(SQLAlchemy, model_class=Base)

    vasques_emission_repository = providers.Singleton(
        vasques_emission_repository.VasquesEmissionRepository, sql_db
    )

    wrf_round_repository = providers.Singleton(
        wrf_round_repository.WRFRoundRepository, sql_db
    )

    remote_wrf_server_connection_settings = providers.Singleton(
        wrf_remote_connection_settings.WRFRemoteConnectionSettings,
        config.hostname,
        config.username,
        config.password,
    )

    ssh_round_namelist_sender = providers.Singleton(
        ssh_round_namelist_sender.SSHRoundNamelistSender,
        remote_wrf_server_connection_settings,
        config.namelist_remote_path,
    )

    rounds_queue = providers.Singleton(Queue)

    wrf_rounds_queue_worker = providers.Singleton(
        wrf_round_processor.WRFRoundProcessor,
        rounds_queue,
        ssh_round_namelist_sender,
    )
