from dataclasses import dataclass
from types import MappingProxyType
from typing import LiteralString


@dataclass
class VehicleSubcategory:
    name: LiteralString
    deterioration_factor: float
    category_consumption: float

    def to_dict(self):
        return MappingProxyType(
            {
                "subcategory_name": self.name,
                "deterioration_factor": self.deterioration_factor,
                "category_consumption": self.category_consumption,
            }
        )
