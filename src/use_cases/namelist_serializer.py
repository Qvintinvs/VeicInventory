from io import StringIO
from types import MappingProxyType
from typing import Union

import f90nml


class NamelistSerializer:
    def __init__(self, namelist_title: str):
        self.__title = namelist_title

    def create_namelist_through(
        self, its_variables: MappingProxyType[str, Union[float, int]]
    ):
        namelist_group = {self.__title: dict(its_variables)}

        with StringIO() as nml_file:
            f90nml.write(namelist_group, nml_file)

            nml_file.seek(0)

            return nml_file.read()
