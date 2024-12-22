from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.vasques_vehicle_model import VasquesVehicleModel, VehicularData


class VehiclesDatabase:
    def __init__(self, db: SQLAlchemy):
        self.__db = db

    def initialize_database_in(self, app: Flask):
        self.__db.init_app(app)

        with app.app_context():
            self.__db.create_all()

    def insert_vehicles_of(self, veic: VehicularData):
        vehicles = VasquesVehicleModel.create_vehicles_from(veic)

        self.__db.session.add_all(vehicles)

        self.__db.session.commit()
