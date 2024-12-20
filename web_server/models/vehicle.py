from collections.abc import Iterable
from typing import NamedTuple

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


class VehicularData(NamedTuple):
    year: Iterable[int]
    fuel: Iterable[str]
    subcategory: Iterable[str]


Base = declarative_base()


class VasquesVehicleModel(Base):
    __tablename__ = "vehicle"

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    fuel = Column(String(50), nullable=False)
    subcategory = Column(String(100), nullable=False)

    def __init__(self, year: int, fuel: str, subcategory: str):
        self.year = year
        self.fuel = fuel
        self.subcategory = subcategory

    @classmethod
    def create_multiple_vehicles_from(cls, vehicles_data: VehicularData):
        years, fuels, subcategories = vehicles_data

        vehicles = (
            cls(year, fuel, subcategory)
            for year, fuel, subcategory in zip(years, fuels, subcategories)
        )

        return vehicles
