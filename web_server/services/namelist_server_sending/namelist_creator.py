from io import StringIO
from typing import LiteralString

import f90nml
from models.vehicle_dict import VehicleDict


class NamelistContentCreator:
    def __init__(self, namelist_title: LiteralString, variables: VehicleDict):
        self.__title = namelist_title
        self.__variables = variables

    def create_namelist(self):
        namelist_group = {self.__title: self.__variables}

        with StringIO() as nml_file:
            f90nml.write(namelist_group, nml_file)

            nml_file.seek(0)

            return nml_file.read()
