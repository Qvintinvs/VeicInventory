from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .base import Base
from .vasques_emission_model import VasquesEmissionModel
from .wrf_round import WRFRound


class VasquesEmissionRoundLink(Base):
    __tablename__ = "vasques_emission_round_link"

    id = Column(Integer, primary_key=True)
    emission_id = Column(Integer, ForeignKey("vehicle.id"), nullable=False)
    wrf_round_id = Column(Integer, ForeignKey("wrf_round.id"), nullable=False)

    emission = relationship(VasquesEmissionModel, backref="round_link")
    wrf_round = relationship(WRFRound, backref="vasques_link")

    def __init__(self, vasques_emission: VasquesEmissionModel, wrf_round: WRFRound):
        self.emission = vasques_emission
        self.wrf_round = wrf_round
