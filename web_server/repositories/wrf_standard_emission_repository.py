from flask_sqlalchemy import SQLAlchemy
from models.wrf_standard_emission import WRFStandardEmission


class WRFStandardEmissionRepository:
    def __init__(self, sql_db: SQLAlchemy):
        self.__db = sql_db

    def save_vehicle_emission(self, emission_data: WRFStandardEmission):
        self.__db.session.add(emission_data)

        self.__db.session.commit()

    def list_emissions(self):
        return self.__db.session.query(WRFStandardEmission).limit(5).all()

    def read_emission_by_id(self, vehicle_emission_id: int):
        return self.__db.session.get(WRFStandardEmission, vehicle_emission_id)

    def delete_data_by_id(self, emission_id: int):
        self.__db.session.query(WRFStandardEmission).filter_by(id=emission_id).delete()

        self.__db.session.commit()
