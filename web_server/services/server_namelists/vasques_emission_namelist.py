from types import MappingProxyType

from models.vasques_emission_model import VasquesEmissionModel

from .match_to_a_namelist_group import match_to_a_namelist_group
from .namelist_content_creator import NamelistContentCreator


class VasquesEmissionNamelist:
    __namelist = NamelistContentCreator("vasques_namelist")

    def __init__(self, variables: VasquesEmissionModel):
        self.__variables = variables

    def create_content(self):
        emission_namelist = {
            "id": self.__variables.id,
            "year": self.__variables.year,
            "fuel": self.__variables.fuel,
            "subcategory": self.__variables.subcategory,
            "exhaust_emission_factor": self.__variables.exhaust_emission_factor,
            "autonomy": self.__variables.autonomy,
        }

        ndict = match_to_a_namelist_group(MappingProxyType(emission_namelist))

        return self.__namelist.create_namelist_through(MappingProxyType(ndict))
