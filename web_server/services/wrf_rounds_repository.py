from flask_sqlalchemy import SQLAlchemy
from models.netcdf_blob import NETCDFBlob
from models.vasques_emission_model import VasquesEmissionModel
from models.wrf_round import WRFRound
from models.wrf_round_status import WRFRoundStatus
from sqlalchemy import DateTime, asc, cast

from .namelist_server_sending.vasques_emission_namelist_creator import (
    VasquesEmissionNamelistCreator,
)
from .round_completion_try_status import RoundCompletionTryStatus


class WRFRoundRepository:
    """Will deal with the database rounds"""

    def __init__(self, sql_db: SQLAlchemy):
        self.__db = sql_db

    def schedule_emission_round(self, vehicle_emission_id: int):
        vehicle_by_id = (
            self.__db.session.query(VasquesEmissionModel)
            .filter_by(id=vehicle_emission_id)
            .first()
        )

        if not vehicle_by_id:
            return

        vehicle_namelist = VasquesEmissionNamelistCreator(vehicle_by_id)

        namelist_content = vehicle_namelist.create_namelist()

        new_round = WRFRound(namelist_content, "output_test")

        self.__db.session.add(new_round)

        self.__db.session.commit()

    def read_oldest_pending_rounds(self):
        rounds_read = (
            self.__db.session.query(WRFRound)
            .filter_by(status=WRFRoundStatus.PENDING)
            .order_by(asc(cast(WRFRound.timestamp, DateTime)))
            .limit(5)
            .all()
        )

        return rounds_read if rounds_read else None

    def get_wrf_round_by_id(self, round_id: int):
        return self.__db.session.query(WRFRound).filter_by(id=round_id).first()

    def try_to_complete_round_with_output(self, processed_netcdf: NETCDFBlob):
        netcdf_scheduler_round: WRFRound | None = processed_netcdf.round

        if not netcdf_scheduler_round:
            return RoundCompletionTryStatus.NOT_FOUND

        try:
            self.__db.session.add(processed_netcdf)

            netcdf_scheduler_round.complete_if_running()

            self.__db.session.commit()

            return RoundCompletionTryStatus.SUCCESS
        except Exception:
            self.__db.session.rollback()

            return RoundCompletionTryStatus.ERROR
