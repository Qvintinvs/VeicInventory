from typing import LiteralString, NamedTuple


class VehicleSubcategory(NamedTuple):
    name: LiteralString | str
    deterioration_factor: float
    category_consumption: float
