from app_container import InventoryAppContainer
from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from services.vehicles_repository import VehiclesRepository
from views.vehicular_inventory_view import VehicularInventoryView


@inject
def register_vehicular_inventory_routes(
    inventory_repo: VehiclesRepository = Provide[
        InventoryAppContainer.vehicular_inventory
    ],
):
    inventory = VehicularInventoryView(inventory_repo)

    inventory_blueprint = Blueprint("vehicular_inventory", __name__)

    inventory_blueprint.add_url_rule(
        "/", view_func=inventory.show_the_page, methods=["GET"]
    )

    inventory_blueprint.add_url_rule(
        "/send_new_vehicle", view_func=inventory.send_new_vehicle, methods=["POST"]
    )

    inventory_blueprint.add_url_rule(
        "/send_id_to_delete", view_func=inventory.send_id_to_delete, methods=["POST"]
    )

    return inventory_blueprint
