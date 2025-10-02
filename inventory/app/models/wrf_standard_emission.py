from django.db import models
from emission_core.models import EmissionManager
from rounds.models import WRFRound

from .cnh_subcategory import CNHSubcategory
from .vehicle_subcategory import VehicleSubcategory


class WRFStandardEmission(models.Model):
    fuel = models.CharField(max_length=50)
    fraction = models.FloatField()
    mileage = models.FloatField()
    note = models.CharField(max_length=256, null=True, blank=True)

    subcategory_name = models.CharField(max_length=50)
    subcategory_deterioration_factor = models.FloatField()
    subcategory_category_consumption = models.FloatField()

    round = models.ForeignKey(
        WRFRound,
        on_delete=models.CASCADE,
        related_name="wrf_standard_emissions",
        null=True,
    )

    objects = models.Manager()
    emissions = EmissionManager()

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
