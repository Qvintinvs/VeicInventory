from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from inventory_app_container import InventoryAppContainer
from repositories.vasques_emission_repository import VasquesEmissionRepository
from views.vasques_emission_view import VasquesEmissionView


@inject
def create_vehicular_inventory_blueprint(
    vasques_emission_repository: VasquesEmissionRepository = Provide[
        InventoryAppContainer.vasques_emission_repository
    ],
):
    inventory = VasquesEmissionView(vasques_emission_repository)

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

    """
    Proposed urls:

    inventory_blueprint.add_url_rule(
        "/edit", view_func=inventory.edit, methods=["POST"]
    )
    """

    return inventory_blueprint
