from flask import Blueprint, redirect, render_template, request, url_for
from services.vehicles_repository import VehiclesRepository
from services.vehicular_data import VehicularData


class MainFormView:
    def __init__(
        self,
        vehicular_inventory: VehiclesRepository,
    ):
        self.__inventory = vehicular_inventory

    def show(self):
        readed_data = self.__inventory.read_vehicles_data()

        tabular_data = tuple(zip(*readed_data))

        return render_template("index.html", vehicular_data=tabular_data)

    def send(self):
        data = request.form

        years = data.getlist("year[]")
        fuels = data.getlist("fuel[]")
        subcategories = data.getlist("subcategory[]")

        years_to_int = map(int, years)

        vehicular_data = VehicularData(years_to_int, fuels, subcategories)

        self.__inventory.insert_vehicles_of(vehicular_data)

        return redirect(url_for("form.show"))

    def add_to(self):
        index_page = Blueprint("form", __name__)

        index_page.add_url_rule("/", view_func=self.show, methods=["GET"])

        index_page.add_url_rule("/send", view_func=self.send, methods=["POST"])

        return index_page
