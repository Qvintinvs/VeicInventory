from django.db import models


class WRFRoundStatus(models.IntegerChoices):
    PENDING = 1, "Pending"
    RUNNING = 2, "Running"
    COMPLETED = 3, "Completed"
    ERROR = 4, "Error"
