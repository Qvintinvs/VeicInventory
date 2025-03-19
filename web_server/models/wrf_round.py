from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Enum, Integer, String, Text

from .base import Base
from .wrf_round_status import WRFRoundStatus


class WRFRound(Base):
    id = Column(Integer, primary_key=True)
    namelist = Column(Text, nullable=False)
    status = Column(Enum(WRFRoundStatus), default=WRFRoundStatus.PENDING)
    output_file_path = Column(String(255))
    timestamp = Column(DateTime, default=datetime.now(UTC))

    def __init__(
        self,
        namelist: str,
        status: WRFRoundStatus,
        output_file_path: str,
        timestamp: datetime,
    ):
        self.namelist = namelist
        self.status = status
        self.output_file_path = output_file_path
        self.timestamp = timestamp
