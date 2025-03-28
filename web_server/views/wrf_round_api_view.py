from flask import Blueprint, jsonify, request
from services.round_completion_try_status import RoundCompletionTryStatus
from services.wrf_rounds_repository import WRFRoundsRepository


class WRFRoundAPIView:
    def __init__(self, rounds_db: WRFRoundsRepository):
        self.__rounds_db = rounds_db

    def complete_the_round(self):
        data = request.json

        if not data or "id" not in data:
            return jsonify({"error": "Missing required field: 'id'"}), 400

        try:
            round_id = int(data.get("id"))
        except ValueError:
            return jsonify({"error": "Invalid ID format. Expected an integer."}), 400

        completion_status: RoundCompletionTryStatus = self.__rounds_db.try_to_complete(
            round_id
        )

        if completion_status == RoundCompletionTryStatus.SUCCESS:
            return jsonify({"message": "Successfully updated round status"}), 200

        if completion_status == RoundCompletionTryStatus.NOT_FOUND:
            return jsonify({"error": "Round ID not found"}), 404

        if completion_status == RoundCompletionTryStatus.ERROR:
            return jsonify(
                {"error": "Failed to update round status in the database"}
            ), 500

    def setup_routes(self):
        wrf_round_api = Blueprint("wrf_round_api", __name__)

        wrf_round_api.add_url_rule(
            "/complete_the_round", view_func=self.complete_the_round, methods=["POST"]
        )

        return wrf_round_api
