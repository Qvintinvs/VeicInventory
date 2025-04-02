from flask import redirect, url_for
from services.wrf_rounds_queue_worker import WRFRoundsQueueWorker
from services.wrf_rounds_repository import WRFRoundsRepository

from .vehicular_inventory_forms.vehicle_interactions_form import VehicleInteractionsForm


class RoundProcessingView:
    def __init__(
        self,
        rounds_repo: WRFRoundsRepository,
        server_sending_queue: WRFRoundsQueueWorker,
    ):
        self.__rounds_repo = rounds_repo
        self.__queue = server_sending_queue

    def process(self):
        process_form: VehicleInteractionsForm = VehicleInteractionsForm()

        if process_form.validate():
            selected_vehicle_id = process_form.action_id

            self.__rounds_repo.schedule_a_round_by_sending(selected_vehicle_id)

            vehicle_id = self.__rounds_repo.get_wrf_round_by(selected_vehicle_id)

            self.__queue.add_to_the_queue(vehicle_id)

        return redirect(url_for("vehicular_inventory.show_the_page"))
