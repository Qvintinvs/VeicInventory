from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from inventory_app_container import InventoryAppContainer
from services.wrf_round_repository import VasquesEmissionRoundRepository
from views.wrf_round_api import VasquesEmissionRoundAPI


@inject
def create_vasques_emission_round_api_blueprint(
    vasques_emission_round_repository: VasquesEmissionRoundRepository = Provide[
        InventoryAppContainer.vasques_emission_round_repository
    ],
):
    wrf_round_api = VasquesEmissionRoundAPI(vasques_emission_round_repository)

    api_blueprint = Blueprint(
        "vasques_emission_round_api", __name__, url_prefix="/vasques_emission_round_api"
    )

    api_blueprint.add_url_rule(
        "/get_round", view_func=wrf_round_api.list_most_urgent_round, methods=["GET"]
    )

    return api_blueprint
