from io import StringIO
from types import MappingProxyType
from typing import LiteralString

import f90nml


class NamelistContentCreator:
    def __init__(self, namelist_title: LiteralString):
        self.__title = namelist_title

    def create_namelist_through(
        self, its_variables: MappingProxyType[str, float | int]
    ):
        namelist_group = {self.__title: dict(its_variables)}

        with StringIO() as nml_file:
            f90nml.write(namelist_group, nml_file)

            nml_file.seek(0)

            return nml_file.read()