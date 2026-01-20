from enum import Enum

from .vehicle_subcategory import VehicleSubcategory


class CNHSubcategory(Enum):
    A = VehicleSubcategory("A", 0.1, 12.5)
    B = VehicleSubcategory("B", 0.15, 14.0)
    C = VehicleSubcategory("C", 0.2, 16.0)
    D = VehicleSubcategory("D", 0.25, 18.0)
    E = VehicleSubcategory("E", 0.3, 20.0)
