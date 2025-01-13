from typing import cast

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

    def __iter__(self):
        yield cast(int, self.id)
        yield cast(int, self.year)
        yield cast(str, self.fuel)
        yield cast(str, self.subcategory)
