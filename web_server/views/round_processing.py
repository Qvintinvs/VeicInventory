from flask import redirect, url_for
from services.vasques_emission_round_repository import VasquesEmissionRoundRepository
from services.wrf_round_processor import WRFRoundProcessor

from .inventory_forms.vehicle_interactions_form import VehicleInteractionsForm


class RoundProcessing:
    def __init__(
        self,
        vasques_emission_round_repository: VasquesEmissionRoundRepository,
        wrf_round_processor: WRFRoundProcessor,
    ):
        self.__repository = vasques_emission_round_repository
        self.__queue = wrf_round_processor

    def process(self):
        process_form: VehicleInteractionsForm = VehicleInteractionsForm()

        if process_form.validate():
            selected_emission_id = process_form.action_id

            self.__repository.schedule_emission_round(selected_emission_id)

            scheduled_round = self.__repository.get_wrf_round_by_id(
                selected_emission_id
            )

            self.__queue.enqueue_round(scheduled_round)

        return redirect(url_for("vehicular_inventory.render_inventory_page"))
