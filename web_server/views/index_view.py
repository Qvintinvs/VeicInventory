from types import MappingProxyType

from flask import Blueprint, render_template, request
from models import vasques_vehicle_model, vehicles_database
from services import namelist_creator


class IndexView:
    def __init__(
        self,
        vehicular_inventory: vehicles_database.VehiclesDatabase,
        namelist_creator: namelist_creator.NamelistContentCreator,
    ):
        self.__inventory = vehicular_inventory
        self.__creator = namelist_creator

    def index(self):
        return render_template("index.html")

    def send(self):
        data = request.form

        years = data.getlist("year[]")
        fuels = data.getlist("fuel[]")
        subcategories = data.getlist("subcategory[]")

        years_to_int = map(int, years)

        vehicular_data = vasques_vehicle_model.VehicularData(
            years_to_int, fuels, subcategories
        )

        self.__inventory.insert_vehicles_of(vehicular_data)

        data_from_namelist_form = MappingProxyType(data)

        namelist_data = self.__creator.create_namelist(data_from_namelist_form)

        return namelist_data

    def add_to(self):
        index_page = Blueprint("index", __name__)

        index_page.add_url_rule("/", view_func=self.index, methods=["GET"])

        index_page.add_url_rule("/send", view_func=self.send, methods=["POST"])

        return index_page
