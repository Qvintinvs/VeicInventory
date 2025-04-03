from flask_sqlalchemy import SQLAlchemy
from models.vasques_emission_model import VasquesEmissionModel


class VasquesEmissionRepository:
    def __init__(self, sql_db: SQLAlchemy):
        self.__db = sql_db

    def insert_vehicle_emission(self, emission_data: VasquesEmissionModel):
        self.__db.session.add(emission_data)

        self.__db.session.commit()

    def read_emission_data(self):
        vehicles_read = self.__db.session.query(VasquesEmissionModel).limit(5).all()

        return vehicles_read

    def delete_data_by_id(self, emission_id: int):
        self.__db.session.query(VasquesEmissionModel).filter_by(id=emission_id).delete()

        self.__db.session.commit()
