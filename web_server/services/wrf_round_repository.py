from flask_sqlalchemy import SQLAlchemy
from models.vasques_emission_model import VasquesEmissionModel
from models.wrf_round import WRFRound
from models.wrf_round_status import WRFRoundStatus
from sqlalchemy import DateTime, asc, cast

from .server_namelists.vasques_emission_namelist import VasquesEmissionNamelist


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

        vehicle_namelist = VasquesEmissionNamelist(vehicle_by_id)

        namelist_content = vehicle_namelist.create_content()

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
        return self.__db.session.get(WRFRound, round_id)
