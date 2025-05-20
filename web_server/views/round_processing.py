import json

import redis
from flask import jsonify, redirect, url_for
from services.vasques_emission_round_repository import VasquesEmissionRoundRepository

from .inventory_forms.vehicle_interactions_form import VehicleInteractionsForm


# TODO: Rename to Round Scheduling
class RoundProcessing:
    def __init__(
        self,
        vasques_emission_round_repository: VasquesEmissionRoundRepository,
        redis_client: redis.Redis,
    ):
        self.__rounds = vasques_emission_round_repository
        self.__redis = redis_client

    def process(self):
        process_form: VehicleInteractionsForm = VehicleInteractionsForm()

        if process_form.validate():
            selected_emission_id = process_form.action_id

            self.__rounds.schedule_emission_round(selected_emission_id)

        return redirect(url_for("vehicular_inventory.render_inventory_page"))

    def send_most_urgent_round(self):
        urgent_round = self.__rounds.read_oldest_pending_rounds()

        if urgent_round is None:
            return jsonify("No rounds at the moment"), 404

        round_json_dict = {
            "id": urgent_round.id,
            "namelist": urgent_round.namelist,
            "output_file_path": urgent_round.output_file_path,
        }

        self.__redis.rpush("wrf-queue", json.dumps(round_json_dict))

        return jsonify(round_json_dict), 200
