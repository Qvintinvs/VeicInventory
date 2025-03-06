from io import StringIO
from types import MappingProxyType
from typing import LiteralString
from .namelist_parser import parse_namelist

import f90nml

ignored_params = ["id"]

class NamelistContentCreator:
    def __init__(self, namelist_title: LiteralString):
        self.__title = namelist_title

    def create_namelist(self, namelist_data: MappingProxyType[str, str]):
        namelist_items = namelist_data.items()
        print(f"namelist_items: {namelist_items}")

        data = {key: value if str(value).strip() else "0" for key, value in namelist_items if key not in ignored_params}
        
        data = parse_namelist(data)
        
        namelist_group = {self.__title: data}
        print(f"namelist_group: {namelist_group}")
        
        with StringIO() as nml_file:
            f90nml.write(namelist_group, nml_file)

            nml_file.seek(0)

            return nml_file.read()
