from django.db import models


class City(models.Model):
    name = models.CharField(max_length=50)
    fuel_consumption = models.FloatField()

    def __init__(self, name: str, fuel_consumption: float):
        self.name = name
        self.fuel_consumption = fuel_consumption
