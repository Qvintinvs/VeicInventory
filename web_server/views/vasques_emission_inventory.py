from flask import redirect, render_template, url_for
from services.vasques_emission_repository import VasquesEmissionRepository
from services.wrf_round_repository import WRFRoundRepository

from .inventory_forms.vasques_emission_form import VasquesEmissionForm
from .inventory_forms.vehicle_interactions_form import VehicleInteractionsForm


class VasquesEmissionInventory:
    def __init__(
        self,
        vehicle_emissions_repository: VasquesEmissionRepository,
        wrf_round_repository: WRFRoundRepository,
    ):
        self.__inventory = vehicle_emissions_repository
        self.__rounds = wrf_round_repository

    def render_inventory_page(self):
        vasques_form: VasquesEmissionForm = VasquesEmissionForm()

        vehicle_emissions = self.__inventory.read_emission_data()

        return render_template(
            "index.html", emission_data=vehicle_emissions, form=vasques_form
        )

    def add_vehicle_emission(self):
        vasques_form: VasquesEmissionForm = VasquesEmissionForm()

        if vasques_form.validate_on_submit():
            vehicle_form_data = vasques_form.vehicle_emission

            self.__inventory.insert_vehicle_emission(vehicle_form_data)

        return redirect(url_for("vehicular_inventory.render_inventory_page"))

    def delete_vehicle_emission(self):
        delete_form: VehicleInteractionsForm = VehicleInteractionsForm()

        if delete_form.validate_on_submit():
            id_to_delete = delete_form.action_id

            self.__inventory.delete_data_by_id(id_to_delete)

        return redirect(url_for("vehicular_inventory.render_inventory_page"))

    def schedule_round(self):
        process_form: VehicleInteractionsForm = VehicleInteractionsForm()

        selected_emission_id = process_form.action_id

        emission_namelist = (
            self.__inventory.read_emission_as_namelist(selected_emission_id)
            if process_form.validate()
            else None
        )

        if emission_namelist:
            persisted_round = self.__inventory.schedule_emission_round(
                emission_namelist
            )

            # TODO: Rename this method and create a function to send to the queue
            self.__rounds.schedule_emission_round(persisted_round)

            self.__rounds.enqueue_pending_round()

        return redirect(url_for("vehicular_inventory.render_inventory_page"))
