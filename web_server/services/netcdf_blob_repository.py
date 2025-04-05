from flask_sqlalchemy import SQLAlchemy
from models.netcdf_blob import NETCDFBlob
from models.wrf_round import WRFRound

from .round_completion_try_status import RoundCompletionTryStatus


class NETCDFBlobRepository:
    def __init__(self, sql_db: SQLAlchemy):
        self.__db = sql_db

    def try_insert_output_for_round(self, netcdf_output: NETCDFBlob):
        wrf_round = self.__db.session.get(WRFRound, netcdf_output.wrf_round_id)

        if not wrf_round:
            return RoundCompletionTryStatus.NOT_FOUND

        try:
            self.__db.session.add(netcdf_output)

            wrf_round.complete_if_running()

            self.__db.session.commit()

            return RoundCompletionTryStatus.SUCCESS
        except Exception:
            self.__db.session.rollback()

            return RoundCompletionTryStatus.ERROR
