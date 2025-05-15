from flask import jsonify
from services.vasques_emission_round_repository import VasquesEmissionRoundRepository


class VasquesEmissionRoundAPI:
    def __init__(
        self, vasques_emission_round_repository: VasquesEmissionRoundRepository
    ):
        self.__rounds = vasques_emission_round_repository

    def list_most_urgent_round(self):
        urgent_round = self.__rounds.read_oldest_pending_rounds()

        if urgent_round is None:
            return jsonify("No rounds at the moment"), 404

        round_json_dict = {
            "id": urgent_round.id,
            "namelist": urgent_round.namelist,
            "output_file_path": urgent_round.output_file_path,
        }

        return jsonify(round_json_dict), 200
