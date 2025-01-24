from models.base import Base
from sqlalchemy import Column, Float, Integer, String


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    city_name = Column(String(50), nullable=False)
    fuel_consumption = Column(Float, nullable=False)
