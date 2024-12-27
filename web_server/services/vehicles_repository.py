from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.vasques_vehicle_model import VasquesVehicleModel
from services.vehicular_data import VehicularData


class VehiclesRepository:
    def __init__(self, sql_db: SQLAlchemy):
        self.__db = sql_db

    def initialize_database_in(self, the_app: Flask):
        self.__db.init_app(the_app)

        with the_app.app_context():
            self.__db.create_all()

    def insert_vehicles_of(self, vehicular_data: VehicularData):
        years, fuels, subcategories = vehicular_data

        vehicles = (
            VasquesVehicleModel(year, fuel, subcategory)
            for year, fuel, subcategory in zip(years, fuels, subcategories)
        )

        self.__db.session.add_all(vehicles)

        self.__db.session.commit()

    def read_vehicles_data(self):
        database_vehicles = self.__db.session.query(VasquesVehicleModel).limit(5).all()

        vehicles_converted_to_data = VehicularData(
            years=(vehicle.year for vehicle in database_vehicles),
            fuels=(vehicle.fuel for vehicle in database_vehicles),
            subcategories=(vehicle.subcategory for vehicle in database_vehicles),
        )

        return vehicles_converted_to_data
