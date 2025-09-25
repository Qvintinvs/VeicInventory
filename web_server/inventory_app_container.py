import minio
import redis
from dependency_injector import containers, providers
from flask_sqlalchemy import SQLAlchemy
from models.base import Base
from repositories import (
    netcdf_blob_repository,
    vasques_emission_repository,
    vasques_round_query_repository,
    wrf_round_command_repository,
    wrf_standard_emission_repository,
    wrfchemi_blobs,
)


class InventoryAppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    sql_db = providers.Singleton(SQLAlchemy, model_class=Base)

    redis_client = providers.Singleton(
        redis.Redis,
        host=config.redis_host,
        port=config.redis_port.as_int(),
        decode_responses=True,
    )

    minio_db = providers.Singleton(
        minio.Minio,
        endpoint="localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False,
    )  # nosec

    vasques_emission_repository = providers.Singleton(
        vasques_emission_repository.VasquesEmissionRepository, sql_db
    )

    wrf_standard_emission_repository = providers.Singleton(
        wrf_standard_emission_repository.WRFStandardEmissionRepository, sql_db
    )

    netcdf_blob_repository = providers.Singleton(
        netcdf_blob_repository.NETCDFBlobRepository, sql_db
    )

    wrf_standard_round_query_repository = providers.Singleton(
        vasques_round_query_repository.WRFStandardRoundQueryRepository, sql_db
    )

    wrf_round_command_repository = providers.Singleton(
        wrf_round_command_repository.WRFRoundCommandRepository, sql_db, redis_client
    )

    wrfchemi_blobs_repository = providers.Singleton(
        wrfchemi_blobs.MinioRepository, minio_db, "wrfchemi-blobs"
    )
