from types import MappingProxyType
from typing import cast

from models.base import Base
from models.city import City
from models.cnh_subcategory import CNHSubcategory
from sqlalchemy import CHAR, Column, Float, Integer, String
from sqlalchemy.orm import composite, relationship


class VasquesVehicleModel(Base):
    __tablename__ = "vehicle"

    id = Column(Integer, primary_key=True)

    year = Column(Integer, nullable=False)
    fuel = Column(String(50), nullable=False)

    autonomy = Column(Float, nullable=False)
    exhaust_emission_factor = Column(Float, nullable=False)

    subcategory = composite(
        CNHSubcategory,
        Column(CHAR, nullable=False),
        Column(Float, nullable=False),
        Column(Float, nullable=False),
    )

    vehicle_city = relationship(City)

    def __init__(
        self,
        year: int,
        fuel: str,
        subcategory: CNHSubcategory,
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

    def to_dict(self):
        return MappingProxyType(
            {
                "id": cast(int, self.id),
                "year": cast(int, self.year),
                "fuel": cast(str, self.fuel),
                "subcategory": self.subcategory.to_dict(),
                "exhaust_emission_factor": cast(float, self.exhaust_emission_factor),
                "autonomy": cast(float, self.autonomy),
            }
        )
