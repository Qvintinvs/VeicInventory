from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from emission_core.models import CNHChoices, FuelChoices
from rounds.models import WRFRound


class City(models.Model):
    name = models.CharField(max_length=50)
    fuel_consumption = models.DecimalField(
        max_digits=5, decimal_places=2, validators=(MinValueValidator(0.0),)
    )


class VasquesEmission(models.Model):
    current_year = timezone.now().date().year

    year = models.PositiveIntegerField(
        validators=(MinValueValidator(1900), MaxValueValidator(current_year + 1))
    )
    fuel = models.CharField(max_length=50, choices=FuelChoices.choices)
    autonomy = models.FloatField(validators=(MinValueValidator(0.0),))
    exhaust_emission_factor = models.FloatField(validators=(MinValueValidator(0.0),))

    subcategory = models.CharField(max_length=1, choices=CNHChoices.choices)

    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="vasques_emissions"
    )

    round = models.ForeignKey(
        WRFRound, on_delete=models.CASCADE, related_name="vasques_emissions", null=True
    )
