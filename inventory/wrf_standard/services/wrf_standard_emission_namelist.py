from types import MappingProxyType
from typing import LiteralString

from models.wrf_round import WRFRound
from models.wrf_standard_emission import WRFStandardEmission

from .namelist_content_creator import NamelistContentCreator


class WRFStandardEmissionNamelist:
    __title: LiteralString = "vasques_emission"

    __namelist = NamelistContentCreator(__title)

    def __init__(self, variables: WRFStandardEmission):
        self.__variables = variables

    def create_round_content(self):
        emission_variables = {
            "fuel": self.__variables.fuel,
            "fraction": self.__variables.fraction,
            "mileage": self.__variables.mileage,
        }

        wrf_format_namelist = self.__namelist.create_namelist_through(
            MappingProxyType(emission_variables)
        )

        return WRFRound(self.__title, wrf_format_namelist, self.__variables)
