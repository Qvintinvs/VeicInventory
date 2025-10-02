from flask_sqlalchemy import SQLAlchemy
from models.wrf_round import WRFRound
from models.wrf_standard_emission import WRFStandardEmission
from services.wrf_standard_emission_namelist import WRFStandardEmissionNamelist


class WRFStandardRoundQueryRepository:
    def __init__(self, sql_db: SQLAlchemy):
        self.__db = sql_db

    # TODO: Let it be more specific to the Rounds
    def list_emissions(self):
        return self.__db.session.query(WRFStandardEmission).limit(5).all()

    def get_round_by_id(self, round_id: int):
        return self.__db.session.get(WRFRound, round_id)

    def generate_round_from_emission(self, emission_id: int):
        emission = self.__db.session.get(WRFStandardEmission, emission_id)

        if emission is None:
            return

        nml = WRFStandardEmissionNamelist(emission)

        round_content = nml.create_round_content()

        emission.add_round(round_content)

        return round_content
