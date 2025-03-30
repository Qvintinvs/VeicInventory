from flask import redirect, render_template, url_for
from services.vehicles_repository import VehiclesRepository

from .vehicular_inventory_forms.vasques_vehicle_form import VasquesVehicleForm
from .vehicular_inventory_forms.vehicle_interactions_form import VehicleInteractionsForm


class VehicularInventoryView:
    def __init__(self, vehicular_inventory: VehiclesRepository):
        self.__inventory = vehicular_inventory

    def show_the_page(self):
        form: VasquesVehicleForm = VasquesVehicleForm()

        vehicle_dicts = self.__inventory.read_vehicles_data()

        return render_template("index.html", vehicular_data=vehicle_dicts, form=form)

    def send_new_vehicle(self):
        form: VasquesVehicleForm = VasquesVehicleForm()

        if form.validate_on_submit():
            vehicle_from_the_form = form.vehicle

            self.__inventory.insert_a(vehicle_from_the_form)

        return redirect(url_for("vehicular_inventory.show_the_page"))

    def send_id_to_delete(self):
        delete_form: VehicleInteractionsForm = VehicleInteractionsForm()

        if delete_form.validate_on_submit():
            id_to_delete = delete_form.action_id

            self.__inventory.delete_vehicle_by(id_to_delete)

        return redirect(url_for("vehicular_inventory.show_the_page"))
