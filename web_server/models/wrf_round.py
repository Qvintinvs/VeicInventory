from datetime import UTC, datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .wrf_round_status import WRFRoundStatus


class WRFRound(Base):
    __tablename__ = "wrf_round"

    id: Mapped[int] = mapped_column(primary_key=True)

    status: Mapped[WRFRoundStatus] = mapped_column(
        Enum(WRFRoundStatus), default=WRFRoundStatus.PENDING, nullable=False
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), nullable=False
    )

    output_file_path: Mapped[str] = mapped_column(String(255), nullable=False)

    namelist: Mapped[str] = mapped_column(Text, nullable=False)

    netcdf_blob = relationship("NETCDFBlob", uselist=True, back_populates="wrf_round")

    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicle.id"))

    vehicle = relationship("VasquesEmissionModel", back_populates="wrf_rounds")

    def __init__(self, output_file_path: str, namelist: str):
        self.output_file_path = output_file_path
        self.namelist = namelist

    def run_if_pending(self):
        if self.status is WRFRoundStatus.PENDING:
            self.status = WRFRoundStatus.RUNNING

    def complete_if_running(self):
        if self.status is WRFRoundStatus.RUNNING:
            self.status = WRFRoundStatus.COMPLETED
            self.timestamp = datetime.now(UTC)
