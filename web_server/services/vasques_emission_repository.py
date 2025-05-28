from flask_sqlalchemy import SQLAlchemy
from models.vasques_emission_model import VasquesEmissionModel

from .server_namelists.vasques_emission_namelist import VasquesEmissionNamelist


class VasquesEmissionRepository:
    def __init__(self, sql_db: SQLAlchemy):
        self.__db = sql_db

    def insert_vehicle_emission(self, emission_data: VasquesEmissionModel):
        self.__db.session.add(emission_data)

        self.__db.session.commit()

    def read_emission_data(self):
        return self.__db.session.query(VasquesEmissionModel).limit(5).all()

    def delete_data_by_id(self, emission_id: int):
        self.__db.session.query(VasquesEmissionModel).filter_by(id=emission_id).delete()

        self.__db.session.commit()

    def read_emission_as_namelist(self, vehicle_emission_id: int):
        emission_read = self.__db.session.get(VasquesEmissionModel, vehicle_emission_id)

        return VasquesEmissionNamelist(emission_read) if emission_read else None
