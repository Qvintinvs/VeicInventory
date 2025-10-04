from django.db import models
from emission_core.models import CNHChoices, EmissionManager
from rounds.models import WRFRound


class City(models.Model):
    name = models.CharField(max_length=50)
    fuel_consumption = models.FloatField()


class VasquesEmission(models.Model):
    year = models.PositiveIntegerField()
    fuel = models.CharField(max_length=50)
    autonomy = models.FloatField()
    exhaust_emission_factor = models.FloatField()

    subcategory = models.CharField(max_length=1, choices=CNHChoices.choices)

    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="vasques_emissions")

    round = models.ForeignKey(
        WRFRound,
        on_delete=models.CASCADE,
        related_name="wrf_standard_emissions",
        null=True,
    )

    objects = models.Manager()
    emissions = EmissionManager()
