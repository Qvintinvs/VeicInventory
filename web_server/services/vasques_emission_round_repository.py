from flask_sqlalchemy import SQLAlchemy
from models.vasques_emission_model import VasquesEmissionModel
from models.wrf_round import WRFRound
from models.wrf_round_status import WRFRoundStatus
from sqlalchemy import asc

from .server_namelists.vasques_emission_namelist import VasquesEmissionNamelist


# TODO: Rename to WRFRoundRepository
class VasquesEmissionRoundRepository:
    """Will deal with the database rounds"""

    def __init__(self, sql_db: SQLAlchemy):
        self.__db = sql_db

    def schedule_emission_round(self, vehicle_emission_id: int):
        vehicle_by_id = self.__db.session.get(VasquesEmissionModel, vehicle_emission_id)

        if not vehicle_by_id:
            return

        namelist_file = VasquesEmissionNamelist(vehicle_by_id)

        new_round = WRFRound("output_test", namelist_file.create_content())

        self.__db.session.add(new_round)

        self.__db.session.commit()

    def read_oldest_pending_rounds(self):
        return (
            self.__db.session.query(WRFRound)
            .filter(WRFRound.status == WRFRoundStatus.PENDING)
            .order_by(asc(WRFRound.timestamp))
            .first()
        )

    def get_wrf_round_by_id(self, round_id: int):
        return self.__db.session.get(WRFRound, round_id)
