from typing import NamedTuple

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

db = SQLAlchemy(model_class=DeclarativeBase)


class VehicularData(NamedTuple):
    year: tuple[int]
    fuel: tuple[str]
    subcategory: tuple[str]


class VasquesVehicleModel(db.Model):
    __tablename__ = "vehicles"

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    fuel = db.Column(db.String(50), nullable=False)
    subcategory = db.Column(db.String(100), nullable=False)

    def __init__(self, year: int, fuel: str, subcategory: str):
        self.year = year
        self.fuel = fuel
        self.subcategory = subcategory

    @classmethod
    def insert_multiple_vehicles_from(cls, vehicles_data: VehicularData):
        years, fuels, subcategories = vehicles_data

        vehicles = (
            cls(year, fuel, subcategory)
            for year, fuel, subcategory in zip(years, fuels, subcategories)
        )

        db.session.add_all(vehicles)

        db.session.commit()
