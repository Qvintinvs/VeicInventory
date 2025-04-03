from app_container import InventoryAppContainer
from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from services.wrf_rounds_repository import WRFRoundRepository
from views.wrf_round_api import WRFRoundAPI


@inject
def register_wrf_round_api_routes(
    wrf_round_repository: WRFRoundRepository = Provide[
        InventoryAppContainer.wrf_round_repository
    ],
):
    wrf_round_api = WRFRoundAPI(wrf_round_repository)

    api_blueprint = Blueprint("wrf_round_api", __name__, url_prefix="/wrf_rounds_api")

    api_blueprint.add_url_rule(
        "/complete_the_round",
        view_func=wrf_round_api.complete_the_round,
        methods=["POST"],
    )

    return api_blueprint
