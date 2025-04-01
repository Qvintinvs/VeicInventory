from typing import cast

from sqlalchemy import CHAR, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import composite, relationship

from .base import Base
from .city import City
from .vehicle_subcategory import VehicleSubcategory
from .vehicle_dict import VehicleDict


class VasquesEmissionModel(Base):
    __tablename__ = "vehicle"

    id = Column(Integer, primary_key=True)

    # year = Column(Integer, nullable=False)
    fuel = Column(String(50), nullable=False)

    subcategory = composite(
        VehicleSubcategory,
        Column(CHAR, nullable=False),
        Column(Float, nullable=False),
        Column(Float, nullable=False),
    )

    autonomy = Column(Float, nullable=False)
    exhaust_emission_factor = Column(Float, nullable=False)
    fraction = Column(Float, nullable=False)
    note = Column(String, nullable=True)

    vehicle_city_key = Column(Integer, ForeignKey(City.id), nullable=False)

    vehicle_city = relationship(City, uselist=False)

    def __init__(
        self,
        # year: int,
        fuel: str,
        subcategory: VehicleSubcategory,
        exhaust_emission_factor: float,
        autonomy: float,
        fraction: float,
        note: str,
        vehicle_city: City,
    ):
        # self.year = year
        self.fuel = fuel
        self.subcategory = subcategory
        self.exhaust_emission_factor = exhaust_emission_factor
        self.autonomy = autonomy
        self.fraction = fraction
        self.note = note
        self.vehicle_city = vehicle_city
        self.vehicle_city_key = vehicle_city.id

    def to_dict(self):
        return VehicleDict(
            id=cast(int, self.id),
            # year=cast(int, self.year),
            fuel=cast(str, self.fuel),
            subcategory=self.subcategory.name,
            exhaust_emission_factor=cast(float, self.exhaust_emission_factor),
            autonomy=cast(float, self.autonomy),
            fraction=cast(float, self.fraction),
            note=cast(str, self.note),
        )
