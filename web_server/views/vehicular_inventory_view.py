from flask import Blueprint, redirect, render_template, url_for
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

    def process(self):
        process_form: VehicleInteractionsForm = VehicleInteractionsForm()

        if process_form.validate_on_submit():
            id_to_process = process_form.action_id

            self.__inventory.send_vehicle_namelist_by(id_to_process)

        return redirect(url_for("vehicular_inventory.show_the_page"))
    
    def edit(self):
        form: VasquesVehicleForm = VasquesVehicleForm()
        form_withid: VehicleInteractionsForm = VehicleInteractionsForm()

        print(form.validate_on_submit())
        print(form_withid.validate_on_submit())

        if form.validate_on_submit() and form_withid.validate_on_submit():
            vehicle_from_the_form = form.vehicle
            action_id = form_withid.action_id
        
            print(f"vehicle_from_the_form: {vehicle_from_the_form}")
            self.__inventory.edit(vehicle_from_the_form.to_dict(), its_id=action_id)
            print(f"form_withid: {form_withid.action_id}")

        return redirect(url_for("vehicular_inventory.show_the_page"))

    def setup_routes(self):
        index_page = Blueprint("vehicular_inventory", __name__)

        index_page.add_url_rule("/", view_func=self.show_the_page, methods=["GET"])

        index_page.add_url_rule(
            "/send_new_vehicle", view_func=self.send_new_vehicle, methods=["POST"]
        )

        index_page.add_url_rule(
            "/send_id_to_delete", view_func=self.send_id_to_delete, methods=["POST"]
        )

        index_page.add_url_rule("/process", view_func=self.process, methods=["POST"])

        index_page.add_url_rule("/edit", view_func=self.edit, methods=["POST"]
        )
        
        return index_page
