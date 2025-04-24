from flask import jsonify
from services.wrf_round_repository import VasquesEmissionRoundRepository


class VasquesEmissionRoundAPI:
    def __init__(
        self, vasques_emission_round_repository: VasquesEmissionRoundRepository
    ):
        self.__rounds = vasques_emission_round_repository

    def list_most_urgent_round(self):
        urgent_round = self.__rounds.read_oldest_pending_rounds()

        if urgent_round is None:
            return jsonify("No rounds at the moment"), 404

        serialized_round_content = urgent_round.create_content()

        return jsonify(serialized_round_content), 200
