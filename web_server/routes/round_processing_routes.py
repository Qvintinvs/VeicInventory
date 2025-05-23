from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from inventory_app_container import InventoryAppContainer
from services.wrf_round_processor import WRFRoundProcessor
from services.wrf_round_repository import WRFRoundRepository
from views.round_processing import RoundProcessing


@inject
def create_round_processing_blueprint(
    wrf_round_repository: WRFRoundRepository = Provide[
        InventoryAppContainer.wrf_round_repository
    ],
    wrf_round_processor: WRFRoundProcessor = Provide[
        InventoryAppContainer.wrf_round_processor
    ],
):
    rounds_view = RoundProcessing(wrf_round_repository, wrf_round_processor)

    rounds_blueprint = Blueprint("round_processing", __name__, url_prefix="/round")

    rounds_blueprint.add_url_rule(
        "/process", view_func=rounds_view.process, methods=["POST"]
    )

    return rounds_blueprint
