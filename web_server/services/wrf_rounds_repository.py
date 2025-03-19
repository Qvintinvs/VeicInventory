from .namelist_server_sending.vasques_emission_namelist_creator import (
    VasquesEmissionNamelistCreator,
)
from .namelist_server_sending.wrf_service import SSHWRFService


class WRFRoundsRepository:
    """Will deal with the database rounds"""

    def __init__(self, wrf_server: SSHWRFService):
        self.__server = wrf_server

    def make_round_with(self, the_database_namelist: VasquesEmissionNamelistCreator):
        self.__server.process_in_the_server(the_database_namelist)
