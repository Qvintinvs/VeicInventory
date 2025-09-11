from typing import TYPE_CHECKING, List

from sqlalchemy import CHAR, Float, String
from sqlalchemy.orm import Mapped, composite, mapped_column, relationship

from .base import Base
from .vehicle_subcategory import VehicleSubcategory

if TYPE_CHECKING:
    from .wrf_round import WRFRound


class WRFStandardEmission(Base):
    __tablename__ = "wrf_standard_emission"

    id: Mapped[int] = mapped_column(primary_key=True)

    fuel: Mapped[str] = mapped_column(String(50), nullable=False)

    subcategory: Mapped[VehicleSubcategory] = composite(
        VehicleSubcategory,
        mapped_column(CHAR, nullable=False),
        mapped_column(Float, nullable=False),
        mapped_column(Float, nullable=False),
    )

    fraction: Mapped[float] = mapped_column(Float, nullable=False)

    mileage: Mapped[float] = mapped_column(Float, nullable=False)

    note: Mapped[str] = mapped_column(String(256), nullable=True)

    wrf_rounds: Mapped[List["WRFRound"]] = relationship(
        "WRFRound", uselist=True, viewonly=True, back_populates="vehicle"
    )

    def __init__(
        self,
        fuel: str,
        subcategory: VehicleSubcategory,
        fraction: float,
        mileage: float,
        note: str,
    ):
        self.fuel = fuel
        self.subcategory = subcategory
        self.fraction = fraction
        self.mileage = mileage
        self.note = note

    def add_round(self, wrf_round: "WRFRound"):
        self.wrf_rounds.append(wrf_round)
