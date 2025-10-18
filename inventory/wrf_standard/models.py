from django.core.validators import MinValueValidator
from django.db import models
from emission_core.models import CNHChoices, FuelChoices
from rounds.models import RoundsPanel


class WRFStandardEmission(models.Model):
    fuel = models.CharField(max_length=50, choices=FuelChoices.choices)
    fraction = models.FloatField(validators=(MinValueValidator(0.0),))
    mileage = models.FloatField(validators=(MinValueValidator(0.0),))
    note = models.CharField(max_length=256, null=True, blank=True)

    subcategory = models.CharField(max_length=1, choices=CNHChoices.choices)

    rounds_panel = models.OneToOneField(
        RoundsPanel,
        on_delete=models.SET_NULL,
        related_name="wrf_standard_emissions",
        null=True,
        editable=False,
    )
