from flask import Blueprint, redirect, render_template, url_for
from services.vehicles_repository import VehiclesRepository
from views.vasques_vehicle_form import VasquesVehicleForm
from views.vehicle_interactions_form import VehicleInteractionsForm


class MainFormView:
    def __init__(self, vehicular_inventory: VehiclesRepository):
        self.__inventory = vehicular_inventory

    def show(self):
        vehicular_form: VasquesVehicleForm = VasquesVehicleForm()

        readed_data = self.__inventory.read_vehicles_data()

        vehicles_to_dict = (vehicle.to_dict() for vehicle in readed_data)

        return render_template(
            "index.html", vehicular_data=vehicles_to_dict, form=vehicular_form
        )

    def send(self):
        form: VasquesVehicleForm = VasquesVehicleForm()

        if form.validate_on_submit():
            new_vehicle = form.vehicle

            self.__inventory.insert_a(new_vehicle)

        return redirect(url_for("form.show"))

    def send_id_to_delete(self):
        delete_form: VehicleInteractionsForm = VehicleInteractionsForm()

        if delete_form.validate_on_submit():
            id_to_delete = delete_form.id

            self.__inventory.delete_vehicle_by(id_to_delete)

        return redirect(url_for("form.show"))

    def add_to(self):
        index_page = Blueprint("form", __name__)

        index_page.add_url_rule("/", view_func=self.show, methods=["GET"])

        index_page.add_url_rule("/send", view_func=self.send, methods=["POST"])

        index_page.add_url_rule(
            "/send_id_to_delete", view_func=self.send_id_to_delete, methods=["POST"]
        )

        return index_page
