from flask import abort, flash, redirect, render_template, url_for
from services.vasques_emission_repository import VasquesEmissionRepository
from services.wrf_round_repository import WRFRoundRepository

from .inventory_forms.vasques_emission_form import VasquesEmissionForm


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

            self.__inventory.save_vehicle_emission(vehicle_form_data)

        return redirect(url_for("vehicular_inventory.render_inventory_page"))

    def delete_vehicle_emission(self, emission_id: int):
        # TODO: return a status value that will be passed to the template
        try:
            self.__inventory.delete_data_by_id(emission_id)
        except Exception:
            flash(f"Emission with ID {emission_id} not found.", "error")

        return redirect(url_for("vehicular_inventory.render_inventory_page"))

    def schedule_emission_round(self):
        self.__rounds.enqueue_pending_round()

        return redirect(url_for("vehicular_inventory.render_inventory_page"))

    def create_round_for_emission(self, emission_id: int):
        emission_namelist = self.__inventory.read_emission_as_namelist(emission_id)

        if emission_namelist is None:
            abort(404, description=f"No emission found for ID {emission_id}")

        emission_round = emission_namelist.create_round_content()

        self.__rounds.save_emission_round(emission_round)

        return self.schedule_emission_round()
