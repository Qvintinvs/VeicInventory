from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.vasques_vehicle_model import VasquesVehicleModel
from .namelist_creator import NamelistContentCreator
from .namelist_sender import send_file


class VehiclesRepository:
    def __init__(self, sql_db: SQLAlchemy):
        self.__db = sql_db

    def initialize_database_in(self, the_app: Flask):
        self.__db.init_app(the_app)

        with the_app.app_context():
            self.__db.create_all()

    def insert_a(self, new_vehicle: VasquesVehicleModel):
        self.__db.session.add(new_vehicle)

        self.__db.session.commit()

    def read_vehicles_data(self):
        vehicles_read = self.__db.session.query(VasquesVehicleModel).limit(5).all()

        return (vehicle.to_dict() for vehicle in vehicles_read)
    
    def send_vehicle_namelist_by(self, its_id: int):
        read_vehicle = self.__db.session.query(VasquesVehicleModel).filter_by(id=its_id).all()
        
        process_dict = [vehicle.to_dict() for vehicle in read_vehicle][0]

        vehicle_namelist = NamelistContentCreator(f"process_{its_id}")

        namelist = vehicle_namelist.create_namelist(process_dict)

        send_file(namelist)

    def delete_vehicle_by(self, its_id: int):
        self.__db.session.query(VasquesVehicleModel).filter_by(id=its_id).delete()

        self.__db.session.commit()
