from typing import cast

from sqlalchemy import CHAR, Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class VasquesVehicleModel(Base):
    __tablename__ = "vehicle"

    id = Column(Integer, primary_key=True)
    _year = Column(Integer, nullable=False)
    _fuel = Column(String(50), nullable=False)
    _subcategory = Column(CHAR, nullable=False)

    def __init__(self, year: int, fuel: str, subcategory: str):
        self._year = year
        self._fuel = fuel
        self._subcategory = subcategory

    @property
    def year(self):
        return cast(int, self._year)

    @property
    def fuel(self):
        return cast(str, self._fuel)

    @property
    def subcategory(self):
        return cast(str, self._subcategory)
