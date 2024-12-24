from models.vehicular_data import VehicularData
from sqlalchemy import CHAR, Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class VasquesVehicleModel(Base):
    __tablename__ = "vehicle"

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    fuel = Column(String(50), nullable=False)
    subcategory = Column(CHAR, nullable=False)

    def __init__(self, year: int, fuel: str, subcategory: str):
        self.year = year
        self.fuel = fuel
        self.subcategory = subcategory

    @classmethod
    def create_vehicles_from(cls, vehicles_data: VehicularData):
        years, fuels, subcategories = vehicles_data

        vehicles = (
            cls(year, fuel, subcategory)
            for year, fuel, subcategory in zip(years, fuels, subcategories)
        )

        return vehicles
