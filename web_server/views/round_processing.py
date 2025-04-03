from flask import redirect, url_for
from services.wrf_rounds_queue_worker import WRFRoundsQueueWorker
from services.wrf_rounds_repository import WRFRoundsRepository

from .inventory_forms.vehicle_interactions_form import VehicleInteractionsForm


class RoundProcessing:
    def __init__(
        self,
        rounds_repository: WRFRoundsRepository,
        server_sending_queue: WRFRoundsQueueWorker,
    ):
        self.__repository = rounds_repository
        self.__queue = server_sending_queue

    def process(self):
        process_form: VehicleInteractionsForm = VehicleInteractionsForm()

        if process_form.validate():
            selected_emission_id = process_form.action_id

            self.__repository.schedule_a_round_by_sending(selected_emission_id)

            scheduled_round = self.__repository.get_wrf_round_by(selected_emission_id)

            self.__queue.add_to_the_queue(scheduled_round)

        return redirect(url_for("vehicular_inventory.render_inventory_page"))
