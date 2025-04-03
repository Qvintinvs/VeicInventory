from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from inventory_app_container import InventoryAppContainer
from views.round_processing import RoundProcessing


@inject
def register_round_processing_routes(
    wrf_round_repository=Provide[InventoryAppContainer.wrf_round_repository],
    wrf_rounds_queue_worker=Provide[InventoryAppContainer.wrf_rounds_queue_worker],
):
    rounds_view = RoundProcessing(wrf_round_repository, wrf_rounds_queue_worker)

    rounds_blueprint = Blueprint("round_processing", __name__, url_prefix="/round")

    rounds_blueprint.add_url_rule(
        "/process", view_func=rounds_view.process, methods=["POST"]
    )

    return rounds_blueprint
