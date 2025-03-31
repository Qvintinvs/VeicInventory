from sqlalchemy import Column, ForeignKey, Integer, LargeBinary
from sqlalchemy.orm import relationship

from .base import Base
from .wrf_round import WRFRound


class NETCDFBlob(Base):
    __tablename__ = "netcdf_blob"

    id = Column(Integer, primary_key=True)
    wrf_round_id = Column(Integer, ForeignKey(WRFRound.id), unique=True)
    netcdf_data = Column(LargeBinary)

    round = relationship(WRFRound, back_populates="blobs")

    def __init__(self, scheduler_round: WRFRound, netcdf_file: bytes):
        self.round = scheduler_round
        self.netcdf_data = netcdf_file
        self.wrf_round_id = scheduler_round.id
