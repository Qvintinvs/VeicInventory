from dataclasses import dataclass
from typing import LiteralString


@dataclass
class VehicleSubcategory:
    name: LiteralString | str
    deterioration_factor: float
    category_consumption: float
