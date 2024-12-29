from flask import Blueprint, render_template, request
from services.vehicles_repository import VehiclesRepository
from services.vehicular_data import VehicularData


class MainFormView:
    def __init__(
        self,
        vehicular_inventory: VehiclesRepository,
    ):
        self.__inventory = vehicular_inventory

    def index(self):
        return render_template("index.html")

    def send(self):
        data = request.form

        years = data.getlist("year[]")
        fuels = data.getlist("fuel[]")
        subcategories = data.getlist("subcategory[]")

        years_to_int = map(int, years)

        vehicular_data = VehicularData(years_to_int, fuels, subcategories)

        self.__inventory.insert_vehicles_of(vehicular_data)

        return render_template("index.html", params=vehicular_data)

    def add_to(self):
        index_page = Blueprint("index", __name__)

        index_page.add_url_rule("/", view_func=self.index, methods=["GET"])

        index_page.add_url_rule("/send", view_func=self.send, methods=["POST"])

        return index_page
