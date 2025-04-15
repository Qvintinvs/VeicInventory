from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import relationship

from .base import Base
from .wrf_round_status import WRFRoundStatus


class WRFRound(Base):
    __tablename__ = "wrf_round"

    id = Column(Integer, primary_key=True)
    status = Column(Enum(WRFRoundStatus), default=WRFRoundStatus.PENDING)
    output_file_path = Column(String(255))
    timestamp = Column(DateTime, default=lambda: datetime.now(UTC))

    blobs = relationship("NETCDFBlob", uselist=True, back_populates="round")

    def __init__(self, output_file_path: str):
        self.output_file_path = output_file_path

    def complete_if_running(self):
        if self.status is WRFRoundStatus.RUNNING:
            self.status = WRFRoundStatus.COMPLETED
            self.timestamp = datetime.now(UTC)
