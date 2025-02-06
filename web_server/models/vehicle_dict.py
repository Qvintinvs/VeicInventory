from typing import TypedDict

from models.cnh_subcategory import VehicleSubcategory


class VehicleDict(TypedDict):
    id: int
    year: int
    fuel: str
    subcategory: VehicleSubcategory
    autonomy: float
    exhaust_emission_factor: float
