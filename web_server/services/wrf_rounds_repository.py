from flask_sqlalchemy import SQLAlchemy
from models.wrf_round import WRFRound

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

        return new_round
