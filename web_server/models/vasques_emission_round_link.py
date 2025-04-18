from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .vasques_emission_model import VasquesEmissionModel
from .wrf_round import WRFRound


class VasquesEmissionRoundLink(Base):
    __tablename__ = "vasques_emission_round_link"

    id: Mapped[int] = mapped_column(primary_key=True)

    emission_id: Mapped[int] = mapped_column(ForeignKey("vehicle.id"), nullable=False)

    wrf_round_id: Mapped[int] = mapped_column(
        ForeignKey("wrf_round.id"), nullable=False
    )

    vasques_emission: Mapped[VasquesEmissionModel] = relationship(
        VasquesEmissionModel, backref="round_link"
    )

    wrf_round: Mapped[WRFRound] = relationship(WRFRound, backref="vasques_link")

    def __init__(self, vasques_emission: VasquesEmissionModel, wrf_round: WRFRound):
        self.vasques_emission = vasques_emission
        self.wrf_round = wrf_round
