from flask_sqlalchemy import SQLAlchemy
from models.vasques_vehicle_model import VasquesVehicleModel, VehicularData


class VehiclesDatabase:
    def __init__(self, db: SQLAlchemy):
        self.__db = db

    def insert_vehicles_of(self, veic: VehicularData):
        vehicles = VasquesVehicleModel.create_vehicles_from(veic)

        self.__db.session.add_all(vehicles)

        self.__db.session.commit()
