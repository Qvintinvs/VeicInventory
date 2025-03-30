from app_container import InventoryAppContainer
from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from services.wrf_rounds_repository import WRFRoundsRepository
from views.wrf_round_api_view import WRFRoundAPIView


@inject
def register_wrf_rounds_api_routes(
    rounds_repo: WRFRoundsRepository = Provide[InventoryAppContainer.wrf_rounds_db],
):
    wrf_round_api = WRFRoundAPIView(rounds_repo)

    api_blueprint = Blueprint("wrf_round_api", __name__)

    api_blueprint.add_url_rule(
        "/complete_the_round",
        view_func=wrf_round_api.complete_the_round,
        methods=["POST"],
    )

    return api_blueprint
