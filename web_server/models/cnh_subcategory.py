from enum import Enum
from types import MappingProxyType
from typing import LiteralString


class CNHSubcategory(Enum):
    A = "A", 0.1, 12.5
    B = "B", 0.15, 14.0
    C = "C", 0.2, 16.0
    D = "D", 0.25, 18.0
    E = "E", 0.3, 20.0

    def __init__(
        self,
        subcategory_name: LiteralString,
        deterioration_factor: float,
        category_consumption: float,
    ):
        self.__name = subcategory_name
        self.__deterioration_factor = deterioration_factor
        self.__category_consumption = category_consumption

    def to_dict(self):
        return MappingProxyType(
            {
                "subcategory_name": self.__name,
                "deterioration_factor": self.__deterioration_factor,
                "category_consumption": self.__category_consumption,
            }
        )
