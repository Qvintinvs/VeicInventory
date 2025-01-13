from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.vasques_vehicle_model import VasquesVehicleModel


class VehiclesRepository:
    def __init__(self, sql_db: SQLAlchemy):
        self.__db = sql_db

    def initialize_database_in(self, the_app: Flask):
        self.__db.init_app(the_app)

        with the_app.app_context():
            self.__db.create_all()

    def insert_a(self, vehicle: VasquesVehicleModel):
        self.__db.session.add(vehicle)

        self.__db.session.commit()

    def read_vehicles_data(self):
        return self.__db.session.query(VasquesVehicleModel).limit(5).all()

    def delete_vehicle_by(self, its_id: int):
        self.__db.session.query(VasquesVehicleModel).filter_by(id=its_id).delete()

        self.__db.session.commit()
