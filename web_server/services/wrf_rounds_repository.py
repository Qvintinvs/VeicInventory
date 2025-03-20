from flask_sqlalchemy import SQLAlchemy
from models.wrf_round import WRFRound

from .namelist_server_sending.vasques_emission_namelist_creator import (
    VasquesEmissionNamelistCreator,
)
from .namelist_server_sending.wrf_service import SSHWRFService


class WRFRoundsRepository:
    """Will deal with the database rounds"""

    def __init__(self, sql_db: SQLAlchemy, wrf_server: SSHWRFService):
        self.__db = sql_db
        self.__server = wrf_server

    def schedule_a_round_by_sending(
        self, the_vehicle_namelist: VasquesEmissionNamelistCreator
    ):
        namelist_content = the_vehicle_namelist.create_namelist()

        new_round = WRFRound(namelist_content, "output_test")

        self.__db.session.add(new_round)

        self.__db.session.commit()

        # does this break the SRP?
        self.__server.process_in_the_server(new_round)
