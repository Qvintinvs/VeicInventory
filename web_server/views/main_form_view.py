from flask import Blueprint, redirect, render_template, request, url_for
from models.vasques_vehicle_model import VasquesVehicleModel
from services.vehicles_repository import VehiclesRepository


class MainFormView:
    def __init__(
        self,
        vehicular_inventory: VehiclesRepository,
    ):
        self.__inventory = vehicular_inventory

    def show(self):
        readed_data = self.__inventory.read_vehicles_data()

        return render_template("index.html", vehicular_data=readed_data)

    def send(self):
        data = request.form

        years = data.get("year[]")
        fuels = data.get("fuel[]")
        subcategories = data.get("subcategory[]")

        years_to_int = int(years)

        vehicular_data = VasquesVehicleModel(years_to_int, fuels, subcategories)

        self.__inventory.insert_a(vehicular_data)

        return redirect(url_for("form.show"))

    def add_to(self):
        index_page = Blueprint("form", __name__)

        index_page.add_url_rule("/", view_func=self.show, methods=["GET"])

        index_page.add_url_rule("/send", view_func=self.send, methods=["POST"])

        return index_page
