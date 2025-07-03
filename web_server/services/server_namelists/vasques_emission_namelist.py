from types import MappingProxyType
from typing import LiteralString

from models.vasques_emission_model import VasquesEmissionModel
from models.wrf_round import WRFRound

from .match_to_a_namelist_group import match_to_a_namelist_group
from .namelist_content_creator import NamelistContentCreator


class VasquesEmissionNamelist:
    __title: LiteralString = "vasques_emission"

    __namelist = NamelistContentCreator(__title)

    def __init__(self, variables: VasquesEmissionModel):
        self.__variables = variables

    def create_round_content(self):
        emission_variables = {
            "year": self.__variables.year,
            "fuel": self.__variables.fuel,
            "subcategory": self.__variables.subcategory,
            "exhaust_emission_factor": self.__variables.exhaust_emission_factor,
            "autonomy": self.__variables.autonomy,
        }

        wrf_format_variables = match_to_a_namelist_group(
            MappingProxyType(emission_variables)
        )

        wrf_format_namelist = self.__namelist.create_namelist_through(
            MappingProxyType(wrf_format_variables)
        )

        return WRFRound(self.__title, wrf_format_namelist, self.__variables)
