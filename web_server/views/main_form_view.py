from flask import Blueprint, redirect, render_template, url_for
from services.vehicles_repository import VehiclesRepository
from views.vasques_vehicle_form import VasquesVehicleForm
from views.vehicle_interactions_form import VehicleInteractionsForm


class MainFormView:
    def __init__(self, vehicular_inventory: VehiclesRepository):
        self.__inventory = vehicular_inventory

    def show(self):
        form: VasquesVehicleForm = VasquesVehicleForm()

        vehicles_dict = self.__inventory.read_vehicles_data()

        return render_template("index.html", vehicular_data=vehicles_dict, form=form)

    def send(self):
        form: VasquesVehicleForm = VasquesVehicleForm()

        if form.validate_on_submit():
            new_vehicle = form.vehicle

            self.__inventory.insert_a(new_vehicle)

        return redirect(url_for("form.show"))

    def send_id_to_delete(self):
        delete_form: VehicleInteractionsForm = VehicleInteractionsForm()

        if delete_form.validate_on_submit():
            id_to_delete = delete_form.action_id

            self.__inventory.delete_vehicle_by(id_to_delete)


        return redirect(url_for("form.show"))

    def process(self):
        process_form: VehicleInteractionsForm = VehicleInteractionsForm()
        print('aaaaa') #test
        if process_form.validate_on_submit():
            id_to_process = process_form.action_id

            self.__inventory.send_vehicle_namelist_by(id_to_process)

        return redirect(url_for("form.show"))

    def add_to(self):
        index_page = Blueprint("form", __name__)

        index_page.add_url_rule("/", view_func=self.show, methods=["GET"])

        index_page.add_url_rule("/send", view_func=self.send, methods=["POST"])

        index_page.add_url_rule(
            "/send_id_to_delete", view_func=self.send_id_to_delete, methods=["POST"]
        )

        index_page.add_url_rule("/process", view_func=self.process, methods=["POST"])

        return index_page
