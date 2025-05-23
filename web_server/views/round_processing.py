from flask import redirect, url_for
from services.wrf_round_processor import WRFRoundProcessor
from services.wrf_round_repository import WRFRoundRepository

from .inventory_forms.vehicle_interactions_form import VehicleInteractionsForm


# TODO: Rename to Round Scheduling
class RoundProcessing:
    def __init__(
        self,
        wrf_round_repository: WRFRoundRepository,
        wrf_round_processor: WRFRoundProcessor,
    ):
        self.__rounds = wrf_round_repository
        self.__processor = wrf_round_processor

    def process(self):
        process_form: VehicleInteractionsForm = VehicleInteractionsForm()

        if process_form.validate():
            selected_emission_id = process_form.action_id

            self.__rounds.schedule_emission_round(selected_emission_id)

        pending_round = self.__rounds.read_oldest_pending_rounds()

        self.__processor.enqueue_round(pending_round)

        return redirect(url_for("vehicular_inventory.render_inventory_page"))
