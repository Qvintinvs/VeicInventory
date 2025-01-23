from types import MappingProxyType
from typing import cast

from sqlalchemy import CHAR, Column, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class VasquesVehicleModel(Base):
    __tablename__ = "vehicle"

    id = Column(Integer, primary_key=True)

    year = Column(Integer, nullable=False)
    fuel = Column(String(50), nullable=False)
    subcategory = Column(CHAR, nullable=False)

    exhaust_emission_factor = Column(Float, nullable=False)
    deterioration_factor = Column(Float, nullable=False)
    autonomy = Column(Float, nullable=False)

    fuel_consumption = Column(Float, nullable=False)
    category_consumption = Column(Float, nullable=False)

    def __init__(
        self,
        year: int,
        fuel: str,
        subcategory: str,
        exhaust_emission_factor: float,
        deterioration_factor: float,
        autonomy: float,
        fuel_consumption: float,
        category_consumption: float,
    ):
        self.year = year
        self.fuel = fuel
        self.subcategory = subcategory
        self.exhaust_emission_factor = exhaust_emission_factor
        self.deterioration_factor = deterioration_factor
        self.autonomy = autonomy
        self.fuel_consumption = fuel_consumption
        self.category_consumption = category_consumption

    def to_dict(self):
        return MappingProxyType(
            {
                "id": cast(int, self.id),
                "year": cast(int, self.year),
                "fuel": cast(str, self.fuel),
                "subcategory": cast(str, self.subcategory),
                "exhaust_emission_factor": cast(float, self.exhaust_emission_factor),
                "deterioration_factor": cast(float, self.deterioration_factor),
                "autonomy": cast(float, self.autonomy),
                "fuel_consumption": cast(float, self.fuel_consumption),
                "category_consumption": cast(float, self.category_consumption),
            }
        )
