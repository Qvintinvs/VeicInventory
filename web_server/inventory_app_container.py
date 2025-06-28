import redis
from dependency_injector import containers, providers
from flask_sqlalchemy import SQLAlchemy
from models.base import Base
from services import (
    netcdf_blob_repository,
    vasques_emission_repository,
    wrf_round_command_repository,
)


class InventoryAppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    sql_db = providers.Singleton(SQLAlchemy, model_class=Base)

    vasques_emission_repository = providers.Singleton(
        vasques_emission_repository.VasquesEmissionRepository, sql_db
    )

    netcdf_blob_repository = providers.Singleton(
        netcdf_blob_repository.NETCDFBlobRepository, sql_db
    )

    # TODO: include the dotenv variables
    redis_client = providers.Singleton(
        redis.Redis, host="localhost", port=6379, decode_responses=True
    )

    wrf_round_command_repository = providers.Singleton(
        wrf_round_command_repository.WRFRoundCommandRepository, sql_db, redis_client
    )
