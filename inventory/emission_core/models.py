from enum import Enum
from typing import LiteralString, NamedTuple

from django.db import models


class VehicleSubcategory(NamedTuple):
    name: LiteralString
    deterioration_factor: float
    category_consumption: float


class CNHSubcategory(Enum):
    A = VehicleSubcategory("A", 0.1, 12.5)
    B = VehicleSubcategory("B", 0.15, 14.0)
    C = VehicleSubcategory("C", 0.2, 16.0)
    D = VehicleSubcategory("D", 0.25, 18.0)
    E = VehicleSubcategory("E", 0.3, 20.0)


class CNHChoices(models.TextChoices):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"


class EmissionManager(models.Manager):
    def list_emissions(self, limit=5):
        return self.all()[:limit]

    def read_emission_by_id(self, emission_id: int):
        return self.filter(id=emission_id).first()

    def delete_data_by_id(self, emission_id: int):
        return self.filter(id=emission_id).delete()
