from datetime import UTC, datetime

from sqlalchemy import DateTime, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .wrf_round_status import WRFRoundStatus


class WRFRound(Base):
    __tablename__ = "wrf_round"

    id: Mapped[int] = mapped_column(primary_key=True)

    status: Mapped[WRFRoundStatus] = mapped_column(
        Enum(WRFRoundStatus), default=WRFRoundStatus.PENDING, nullable=False
    )

    output_file_path: Mapped[str] = mapped_column(String(255), nullable=False)

    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), nullable=False
    )

    blobs = relationship("NETCDFBlob", uselist=True, back_populates="wrf_round")

    def __init__(self, output_file_path: str):
        self.output_file_path = output_file_path

    def complete_if_running(self):
        if self.status is WRFRoundStatus.RUNNING:
            self.status = WRFRoundStatus.COMPLETED
            self.timestamp = datetime.now(UTC)
