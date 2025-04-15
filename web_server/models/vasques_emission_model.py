from sqlalchemy import CHAR, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, composite, mapped_column, relationship

from .base import Base
from .city import City
from .vehicle_subcategory import VehicleSubcategory


class VasquesEmissionModel(Base):
    __tablename__ = "vehicle"

    id: Mapped[int] = mapped_column(primary_key=True)

    year: Mapped[int] = mapped_column(nullable=False)

    fuel: Mapped[str] = mapped_column(String(50), nullable=False)

    subcategory: Mapped[VehicleSubcategory] = composite(
        VehicleSubcategory,
        mapped_column(CHAR, nullable=False),
        mapped_column(Float, nullable=False),
        mapped_column(Float, nullable=False),
    )

    autonomy: Mapped[float] = mapped_column(nullable=False)

    exhaust_emission_factor: Mapped[float] = mapped_column(nullable=False)

    vehicle_city_key: Mapped[int] = mapped_column(ForeignKey(City.id), nullable=False)

    vehicle_city: Mapped[City] = relationship(City, uselist=False)

    def __init__(
        self,
        year: int,
        fuel: str,
        subcategory: VehicleSubcategory,
        exhaust_emission_factor: float,
        autonomy: float,
        vehicle_city: City,
    ):
        self.year = year
        self.fuel = fuel
        self.subcategory = subcategory
        self.exhaust_emission_factor = exhaust_emission_factor
        self.autonomy = autonomy
        self.vehicle_city = vehicle_city
