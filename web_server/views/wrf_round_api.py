from io import BytesIO

from flask import jsonify, request
from models.netcdf_blob import NETCDFBlob
from services.round_completion_try_status import RoundCompletionTryStatus
from services.wrf_rounds_repository import WRFRoundsRepository


class WRFRoundAPI:
    def __init__(self, rounds_repository: WRFRoundsRepository):
        self.__rounds_db = rounds_repository

    def complete_the_round(self):
        round_id = request.form.get("id")

        if not round_id:
            return jsonify({"error": "Missing required field: 'id'"}), 400

        try:
            round_id = int(round_id)
        except ValueError:
            return jsonify({"error": "Invalid ID format. Expected an integer."}), 400

        requested_round = self.__rounds_db.get_wrf_round_by(round_id)

        if not requested_round:
            return jsonify({"error": "Round ID not found"}), 404

        file = request.files["file"]

        file_bytes = BytesIO(file.read())

        blob = NETCDFBlob(file_bytes.getvalue(), requested_round)

        completion_status: RoundCompletionTryStatus = (
            self.__rounds_db.try_to_complete_round_of(blob)
        )

        if completion_status == RoundCompletionTryStatus.SUCCESS:
            return jsonify({"message": "Successfully updated round status"}), 200

        # Get rid of this if statement
        if completion_status == RoundCompletionTryStatus.NOT_FOUND:
            return jsonify({"error": "Round ID not found"}), 404

        if completion_status == RoundCompletionTryStatus.ERROR:
            return jsonify(
                {"error": "Failed to update round status in the database"}
            ), 500
