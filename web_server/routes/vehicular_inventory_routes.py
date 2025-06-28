from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from inventory_app_container import InventoryAppContainer
from services.vasques_emission_repository import VasquesEmissionRepository
from views.vasques_emission_inventory import VasquesEmissionInventory


@inject
def create_vehicular_inventory_blueprint(
    vasques_emission_repository: VasquesEmissionRepository = Provide[
        InventoryAppContainer.vasques_emission_repository
    ],
):
    inventory = VasquesEmissionInventory(vasques_emission_repository)

    inventory_blueprint = Blueprint("vehicular_inventory", __name__)

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

    return inventory_blueprint
