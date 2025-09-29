from django.db import models

from .wrf_round_status import WRFRoundStatus
from .wrf_standard_emission import WRFStandardEmission


class WRFRound(models.Model):
    status: models.IntegerField[WRFRoundStatus, int] = models.IntegerField(
        choices=WRFRoundStatus.choices, default=WRFRoundStatus.PENDING
    )
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=True)
    output_file_path = models.CharField(max_length=255, blank=False)
    namelist = models.TextField(blank=False)

    vehicle = models.ForeignKey(
        WRFStandardEmission,
        on_delete=models.CASCADE,
        related_name="wrf_rounds",
    )

    def __init__(
        self, output_file_path: str, namelist: str, vehicle: WRFStandardEmission
    ):
        self.output_file_path = output_file_path
        self.namelist = namelist
        self.vehicle = vehicle

    def run_if_pending(self):
        if self.status == WRFRoundStatus.PENDING:
            self.status = WRFRoundStatus.RUNNING
            self.save(update_fields="status")

    def complete_if_running(self):
        if self.status == WRFRoundStatus.RUNNING:
            self.status = WRFRoundStatus.COMPLETED
            self.save(update_fields=("status", "timestamp"))
