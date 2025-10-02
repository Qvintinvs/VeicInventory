from django.db import models

from .wrf_round import WRFRound


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
