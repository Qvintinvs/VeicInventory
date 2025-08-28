from flask_sqlalchemy import SQLAlchemy
from models.vasques_emission_model import VasquesEmissionModel
from models.wrf_round import WRFRound
from services.vasques_emission_namelist import VasquesEmissionNamelist


class VasquesRoundQueryRepository:
    def __init__(self, sql_db: SQLAlchemy):
        self.__db = sql_db

    # TODO: Let it be more specific to the Rounds
    def list_emissions(self):
        return self.__db.session.query(VasquesEmissionModel).limit(5).all()

    def get_round_by_id(self, round_id: int):
        return self.__db.session.get(WRFRound, round_id)

    def generate_round_from_emission(self, emission_id: int):
        emission = self.__db.session.get(VasquesEmissionModel, emission_id)

        if emission is None:
            return

        nml = VasquesEmissionNamelist(emission)

        round_content = nml.create_round_content()

        emission.add_round(round_content)

        return round_content
