import json

import redis
from models.wrf_round import WRFRound


# TODO: Rename queue
# TODO: Add exceptions handling
class WRFRoundProcessor:
    def __init__(self, redis_client: redis.Redis):
        self.__redis = redis_client

    def enqueue_round(self, wrf_round: WRFRound):
        round_json_dict = {
            "id": wrf_round.id,
            "namelist": wrf_round.namelist,
            "output_file_path": wrf_round.output_file_path,
        }

        self.__redis.rpush("wrf-queue", json.dumps(round_json_dict))

    def retrieve_round_completeness(self):
        raise NotImplementedError()
