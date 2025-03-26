from flask_sqlalchemy import SQLAlchemy
from models.wrf_round import WRFRound
from models.wrf_round_status import WRFRoundStatus

from .namelist_server_sending.vasques_emission_namelist_creator import (
    VasquesEmissionNamelistCreator,
)


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

    def try_to_complete(self, a_running_round_id: int):
        wrf_round = (
            self.__db.session.query(WRFRound).filter_by(id=a_running_round_id).first()
        )

        if not wrf_round:
            return

        try:
            wrf_round.complete_if_running()

            self.__db.session.commit()
        except Exception:
            self.__db.session.rollback()
