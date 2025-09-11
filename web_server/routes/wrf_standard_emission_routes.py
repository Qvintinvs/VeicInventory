from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from inventory_app_container import InventoryAppContainer
from repositories.wrf_standard_emission_repository import WRFStandardEmissionRepository
from views.wrf_standard_emission_view import WRFStandardEmissionView


@inject
def create_wrf_standard_emission_blueprint(
    wrf_standard_emission_repository: WRFStandardEmissionRepository = Provide[
        InventoryAppContainer.wrf_standard_emission_repository
    ],
):
    inventory = WRFStandardEmissionView(wrf_standard_emission_repository)

    inventory_blueprint = Blueprint("wrf_standard", __name__)

    inventory_blueprint.add_url_rule(
        "/", view_func=inventory.render_inventory_page, methods=["GET"]
    )

    inventory_blueprint.add_url_rule(
        "/add_vehicle_emission",
        view_func=inventory.add_vehicle_emission,
        methods=["POST"],
    )

    inventory_blueprint.add_url_rule(
        "/delete_vehicle_emission/<int:emission_id>",
        view_func=inventory.delete_vehicle_emission,
        methods=["POST"],
    )

    inventory_blueprint.add_url_rule(
        "/get_netcdf_data", view_func=inventory.get_netcdf_data, methods=["GET"]
    )

    inventory_blueprint.add_url_rule(
        "/visualize", view_func=inventory.visualize, methods=["GET"]
    )

    """
    Proposed urls:

    inventory_blueprint.add_url_rule(
        "/edit", view_func=inventory.edit, methods=["POST"]
    )
    """

    return inventory_blueprint
