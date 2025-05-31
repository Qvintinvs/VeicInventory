import json

import redis
from flask_sqlalchemy import SQLAlchemy
from models.wrf_round import WRFRound
from models.wrf_round_status import WRFRoundStatus


class WRFRoundRepository:
    """Will deal with the database rounds"""

    def __init__(self, sql_db: SQLAlchemy, redis_client: redis.Redis):
        self.__db = sql_db
        self.__redis = redis_client

    def save_emission_round(self, new_round: WRFRound):
        self.__db.session.add(new_round)

        self.__db.session.commit()

    def schedule_pending_round(self, pending_round: WRFRound):
        round_json_dict = {
            "id": pending_round.id,
            "namelist": pending_round.namelist,
            "output_file_path": pending_round.output_file_path,
        }

        self.__redis.rpush("wrf-queue", json.dumps(round_json_dict))

        pending_round.status = WRFRoundStatus.RUNNING

        self.__db.session.commit()

    def get_wrf_round_by_id(self, round_id: int):
        return self.__db.session.get(WRFRound, round_id)
