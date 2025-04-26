from flask_sqlalchemy import SQLAlchemy
from models.vasques_emission_model import VasquesEmissionModel
from models.vasques_emission_round_link import VasquesEmissionRoundLink
from models.wrf_round import WRFRound
from models.wrf_round_status import WRFRoundStatus
from sqlalchemy import asc

from .server_namelists.vasques_emission_namelist import VasquesEmissionNamelist


class VasquesEmissionRoundRepository:
    """Will deal with the database rounds"""

    def __init__(self, sql_db: SQLAlchemy):
        self.__db = sql_db

    def schedule_emission_round(self, vehicle_emission_id: int):
        vehicle_by_id = self.__db.session.get(VasquesEmissionModel, vehicle_emission_id)

        if not vehicle_by_id:
            return

        new_round = WRFRound("output_test")

        link = VasquesEmissionRoundLink(vehicle_by_id, new_round)

        self.__db.session.add(link)

        self.__db.session.commit()

    def read_oldest_pending_rounds(self):
        link = (
            self.__db.session.query(VasquesEmissionRoundLink)
            .join(VasquesEmissionRoundLink.wrf_round)
            .filter(WRFRound.status == WRFRoundStatus.PENDING)
            .order_by(asc(WRFRound.timestamp))
            .first()
        )

        return VasquesEmissionNamelist(link.vasques_emission) if link else None

    def get_wrf_round_by_id(self, round_id: int):
        return self.__db.session.get(WRFRound, round_id)
