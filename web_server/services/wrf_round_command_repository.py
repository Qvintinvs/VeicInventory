import json

import redis
from flask_sqlalchemy import SQLAlchemy
from models.wrf_round import WRFRound


class WRFRoundCommandRepository:
    """Will deal with the database rounds"""

    def __init__(self, sql_db: SQLAlchemy, redis_client: redis.Redis):
        self.__db = sql_db
        self.__redis = redis_client

    def save_emission_round(self, emission_round: WRFRound):
        self.__db.session.add(emission_round)

        self.__db.session.commit()

    def publish_pending_round(self, pending_round: WRFRound):
        serialized_round = {
            "id": pending_round.id,
            "namelist": pending_round.namelist,
            "output_file_path": pending_round.output_file_path,
        }

        round_json_dict = json.dumps(serialized_round)

        self.__redis.rpush("wrf-queue", round_json_dict)

        pending_round.run_if_pending()

        self.__db.session.commit()
