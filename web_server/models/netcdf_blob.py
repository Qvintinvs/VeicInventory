from sqlalchemy import ForeignKey, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .wrf_round import WRFRound


class NETCDFBlob(Base):
    __tablename__ = "netcdf_blob"

    id: Mapped[int] = mapped_column(primary_key=True)

    wrf_round_id: Mapped[int] = mapped_column(
        ForeignKey(WRFRound.id), unique=True, nullable=False
    )

    netcdf_data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    wrf_round: Mapped[WRFRound] = relationship(WRFRound, back_populates="netcdf_blob")

    def __init__(self, netcdf_file: bytes, scheduler_round_id: int):
        self.netcdf_data = netcdf_file
        self.wrf_round_id = scheduler_round_id
