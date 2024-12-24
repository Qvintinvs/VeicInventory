from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.vasques_vehicle_model import VasquesVehicleModel
from models.vehicular_data import VehicularData


class VehiclesDatabase:
    def __init__(self, sql_db: SQLAlchemy):
        self.__db = sql_db

    def initialize_database_in(self, the_app: Flask):
        self.__db.init_app(the_app)

        with the_app.app_context():
            self.__db.create_all()

    def insert_vehicles_of(self, vehicular_data: VehicularData):
        vehicles = VasquesVehicleModel.create_vehicles_from(vehicular_data)

        self.__db.session.add_all(vehicles)

        self.__db.session.commit()

    def read_vehicles(self):
        return self.__db.session.query(VasquesVehicleModel).limit(5).all()
