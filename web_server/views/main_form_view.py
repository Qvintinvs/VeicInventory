from flask import Blueprint, redirect, render_template, request, url_for
from models.vasques_vehicle_model import VasquesVehicleModel
from services.vehicles_repository import VehiclesRepository
from views.vasques_vehicle_form import VasquesVehicleForm


class MainFormView:
    def __init__(
        self,
        vehicular_inventory: VehiclesRepository,
    ):
        self.__inventory = vehicular_inventory

    def show(self):
        readed_data = self.__inventory.read_vehicles_data()

        vehicular_form: VasquesVehicleForm = VasquesVehicleForm()

        return render_template(
            "index.html", vehicular_data=readed_data, form=vehicular_form
        )

    def send(self):
        form: VasquesVehicleForm = VasquesVehicleForm(request.form)

        if form.validate_on_submit():
            new_vehicle = VasquesVehicleModel(
                form.year.data, form.fuel.data, form.subcategory.data
            )

            self.__inventory.insert_a(new_vehicle)

        return redirect(url_for("form.show"))

    def add_to(self):
        index_page = Blueprint("form", __name__)

        index_page.add_url_rule("/", view_func=self.show, methods=["GET"])

        index_page.add_url_rule("/send", view_func=self.send, methods=["POST"])

        return index_page
