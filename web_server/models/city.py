from .base import Base
from sqlalchemy import Column, Float, Integer, String


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    fuel_consumption = Column(Float, nullable=False)

    def __init__(self, name: str, fuel_consumption: float):
        self.name = name
        self.fuel_consumption = fuel_consumption
