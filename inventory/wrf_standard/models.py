from django.db import models
from emission_core.models import CNHChoices, EmissionManager
from rounds.models import WRFRound


class WRFStandardEmission(models.Model):
    fuel = models.CharField(max_length=50)
    fraction = models.FloatField()
    mileage = models.FloatField()
    note = models.CharField(max_length=256, null=True, blank=True)

    subcategory = models.CharField(max_length=1, choices=CNHChoices.choices)

    round = models.ForeignKey(
        WRFRound,
        on_delete=models.CASCADE,
        related_name="wrf_standard_emissions",
        null=True,
    )

    objects = models.Manager()
    emissions = EmissionManager()
