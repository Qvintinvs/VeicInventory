from app_container import InventoryAppContainer
from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from views.round_processing_view import RoundProcessingView


@inject
def register_round_processing_routes(
    rounds_repo=Provide[InventoryAppContainer.wrf_rounds_db],
    worker=Provide[InventoryAppContainer.wrf_rounds_queue_worker],
):
    rounds_view = RoundProcessingView(rounds_repo, worker)

    inventory_blueprint = Blueprint("rounds_processing", __name__)

    inventory_blueprint.add_url_rule(
        "/process", view_func=rounds_view.process, methods=["POST"]
    )

    return inventory_blueprint
