from django.db import models


class WRFRoundStatus(models.IntegerChoices):
    PENDING = 1, "Pending"
    RUNNING = 2, "Running"
    COMPLETED = 3, "Completed"
    ERROR = 4, "Error"


class WRFRound(models.Model):
    status = models.IntegerField(
        choices=WRFRoundStatus.choices, default=WRFRoundStatus.PENDING
    )
    timestamp = models.DateTimeField(auto_now=True)
    output_file_path = models.CharField(max_length=255, blank=False)
    namelist = models.TextField(blank=False)

    def __init__(self, output_file_path: str, namelist: str):
        self.output_file_path = output_file_path
        self.namelist = namelist

    def run_if_pending(self):
        if self.status == WRFRoundStatus.PENDING:
            self.status = WRFRoundStatus.RUNNING
            self.save(update_fields="status")

    def complete_if_running(self):
        if self.status == WRFRoundStatus.RUNNING:
            self.status = WRFRoundStatus.COMPLETED
            self.save(update_fields=("status", "timestamp"))


class NETCDFBlob(models.Model):
    wrf_round = models.OneToOneField(
        WRFRound,
        on_delete=models.CASCADE,
        related_name="netcdf_blob",
    )
    netcdf_data = models.BinaryField()

    def __init__(self, netcdf_file: bytes, scheduler_round_id: int):
        self.netcdf_data = netcdf_file
        self.wrf_round_id = scheduler_round_id
