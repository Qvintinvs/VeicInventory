from enum import auto

from django.db import models


class RoundStatus(models.IntegerChoices):
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    ERROR = auto()


class WRFRound(models.Model):
    status = models.IntegerField(
        choices=RoundStatus.choices, default=RoundStatus.PENDING
    )
    timestamp = models.DateTimeField(auto_now=True)
    output_file_path = models.CharField(max_length=255, blank=False)
    namelist = models.TextField(blank=False)

    def run_if_pending(self):
        if self.status == RoundStatus.PENDING:
            self.status = RoundStatus.RUNNING
            self.save(update_fields="status")

    def complete_if_running(self):
        if self.status == RoundStatus.RUNNING:
            self.status = RoundStatus.COMPLETED
            self.save(update_fields=("status", "timestamp"))


class NETCDFBlob(models.Model):
    wrf_round = models.OneToOneField(
        WRFRound,
        on_delete=models.CASCADE,
        related_name="netcdf_blob",
    )
    netcdf_data = models.BinaryField()
