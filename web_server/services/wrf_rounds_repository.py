from flask_sqlalchemy import SQLAlchemy
from models.wrf_round import WRFRound
from models.wrf_round_status import WRFRoundStatus

from .namelist_server_sending.vasques_emission_namelist_creator import (
    VasquesEmissionNamelistCreator,
)
from .round_completion_try_status import RoundCompletionTryStatus


class WRFRoundsRepository:
    """Will deal with the database rounds"""

    def __init__(self, sql_db: SQLAlchemy):
        self.__db = sql_db

    def schedule_a_round_by_sending(
        self, the_vehicle_namelist: VasquesEmissionNamelistCreator
    ):
        namelist_content = the_vehicle_namelist.create_namelist()

        new_round = WRFRound(namelist_content, "output_test")

        self.__db.session.add(new_round)

        self.__db.session.commit()

    def read_earliest_not_processed_rounds(self):
        rounds_read = (
            self.__db.session.query(WRFRound)
            .filter_by(status=WRFRoundStatus.PENDING)
            .order_by(WRFRound.timestamp.asc())
            .limit(5)
            .all()
        )

        return rounds_read if rounds_read else None

    def get_wrf_round_by(self, its_id: int):
        return self.__db.session.query(WRFRound).filter_by(id=its_id).first()

    def try_to_complete(self, a_running_round_by_id: int):
        wrf_round = self.get_wrf_round_by(a_running_round_by_id)

        if not wrf_round:
            return RoundCompletionTryStatus.NOT_FOUND

        try:
            wrf_round.complete_if_running()

            self.__db.session.commit()

            return RoundCompletionTryStatus.SUCCESS
        except Exception:
            self.__db.session.rollback()

            return RoundCompletionTryStatus.ERROR
