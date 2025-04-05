from io import BytesIO

from flask import jsonify, request
from models.netcdf_blob import NETCDFBlob
from services.netcdf_blob_repository import NETCDFBlobRepository
from services.round_completion_try_status import RoundCompletionTryStatus


class WRFRoundAPI:
    def __init__(self, netcdf_blob_repository: NETCDFBlobRepository):
        self.__blob_storage = netcdf_blob_repository

    def complete_the_round(self):
        round_id = request.form.get("id")

        if not round_id:
            return jsonify({"error": "Missing required field: 'id'"}), 400

        try:
            round_id = int(round_id)
        except ValueError:
            return jsonify({"error": "Invalid ID format. Expected an integer."}), 400

        if round_id < 0:
            return jsonify(
                {"error": "Invalid ID format. Expected a positive integer."}
            ), 400

        file = request.files["file"]

        file_bytes = BytesIO(file.read())

        blob = NETCDFBlob(file_bytes.getvalue(), round_id)

        completion_status: RoundCompletionTryStatus = (
            self.__blob_storage.try_insert_output_for_round(blob)
        )

        if completion_status == RoundCompletionTryStatus.SUCCESS:
            return jsonify({"message": "Successfully updated round status"}), 200

        if completion_status == RoundCompletionTryStatus.NOT_FOUND:
            return jsonify({"error": "Round ID not found"}), 404

        if completion_status == RoundCompletionTryStatus.ERROR:
            return jsonify(
                {"error": "Failed to update round status in the database"}
            ), 500
