from typing import TYPE_CHECKING

from django.db import models

from .cnh_subcategory import CNHSubcategory
from .vehicle_subcategory import VehicleSubcategory

if TYPE_CHECKING:
    from .wrf_round import WRFRound


class WRFStandardEmission(models.Model):
    fuel = models.CharField(max_length=50)
    fraction = models.FloatField()
    mileage = models.FloatField()
    note = models.CharField(max_length=256, null=True, blank=True)

    subcategory_name: models.CharField[str, str] = models.CharField(max_length=50)
    subcategory_deterioration_factor = models.FloatField()
    subcategory_category_consumption = models.FloatField()

    def __init__(
        self,
        fuel: str,
        subcategory: CNHSubcategory,
        fraction: float,
        mileage: float,
        note: str,
    ):
        self.fuel = fuel
        self.subcategory = subcategory
        self.fraction = fraction
        self.mileage = mileage
        self.note = note

    @property
    def subcategory(self):
        return VehicleSubcategory(
            name=self.subcategory_name,
            deterioration_factor=self.subcategory_deterioration_factor,
            category_consumption=self.subcategory_category_consumption,
        )

    @subcategory.setter
    def subcategory(self, subcategory: CNHSubcategory):
        self.subcategory_name = subcategory.value.name
        self.subcategory_deterioration_factor = subcategory.value.deterioration_factor
        self.subcategory_category_consumption = subcategory.value.category_consumption

    def add_round(self, wrf_round: "WRFRound"):
        wrf_round.vehicle = self
        wrf_round.save()
