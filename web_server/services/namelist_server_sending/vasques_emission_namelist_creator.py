from types import MappingProxyType
from typing import cast

from models.vasques_emission_model import VasquesEmissionModel

from .namelist_creator import NamelistContentCreator


class VasquesEmissionNamelistCreator:
    __namelist = NamelistContentCreator("vasques_namelist")

    def __init__(self, variables: VasquesEmissionModel):
        self.__variables = variables

    def create_namelist(self):
        emission_namelist = {
            "id": cast(int, self.__variables.id),
            "year": cast(int, self.__variables.year),
            "exhaust_emission_factor": cast(
                float, self.__variables.exhaust_emission_factor
            ),
            "autonomy": cast(float, self.__variables.autonomy),
        }

        return self.__namelist.create_namelist_through(
            MappingProxyType(emission_namelist)
        )
