from multiprocessing import Queue

from dependency_injector import containers, providers
from flask_sqlalchemy import SQLAlchemy
from models.base import Base
from services import (
    netcdf_blob_repository,
    ssh_round_namelist_sender,
    vasques_emission_repository,
    vasques_emission_round_repository,
    wrf_remote_connection_settings,
    wrf_round_processor,
)


class InventoryAppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    sql_db = providers.Singleton(SQLAlchemy, model_class=Base)

    vasques_emission_repository = providers.Singleton(
        vasques_emission_repository.VasquesEmissionRepository, sql_db
    )

    vasques_emission_round_repository = providers.Singleton(
        vasques_emission_round_repository.VasquesEmissionRoundRepository, sql_db
    )

    wrf_remote_connection_settings = providers.Singleton(
        wrf_remote_connection_settings.WRFRemoteConnectionSettings,
        config.hostname,
        config.username,
        config.password,
    )

    ssh_round_namelist_sender = providers.Singleton(
        ssh_round_namelist_sender.SSHRoundNamelistSender,
        wrf_remote_connection_settings,
        config.namelist_remote_path,
    )

    rounds_queue = providers.Singleton(Queue)

    wrf_round_processor = providers.Singleton(
        wrf_round_processor.WRFRoundProcessor,
        rounds_queue,
        ssh_round_namelist_sender,
    )

    netcdf_blob_repository = providers.Singleton(
        netcdf_blob_repository.NETCDFBlobRepository, sql_db
    )
