from types import MappingProxyType

from models.vehicle_dict import VehicleDict

from .namelist_creator import NamelistContentCreator


class VasquesNamelistCreator:
    __namelist = NamelistContentCreator("vasques_namelist")

    def __init__(self, variables: VehicleDict):
        self.__variables = variables

    def create_namelist(self):
        acid = MappingProxyType({"factor": self.__variables["year"]})

        return self.__namelist.create_namelist_through(acid)
