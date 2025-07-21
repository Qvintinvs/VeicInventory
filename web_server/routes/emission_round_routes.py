from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from inventory_app_container import InventoryAppContainer
from services.vasques_round_query_repository import VasquesRoundQueryRepository
from services.wrf_round_command_repository import WRFRoundCommandRepository
from views.emission_round_view import EmissionRoundView


@inject
def create_emission_round_blueprint(
    vasques_round_query_repository: VasquesRoundQueryRepository = Provide[
        InventoryAppContainer.vasques_round_query_repository
    ],
    wrf_round_command_repository: WRFRoundCommandRepository = Provide[
        InventoryAppContainer.wrf_round_command_repository
    ],
):
    emission_round_view = EmissionRoundView(
        vasques_round_query_repository, wrf_round_command_repository
    )

    emission_round_blueprint = Blueprint("emission_round", __name__)

    emission_round_blueprint.add_url_rule(
        "/",
        view_func=emission_round_view.render_emission_selection_page,
        methods=["GET"],
    )

    emission_round_blueprint.add_url_rule(
        "/schedule_emission_round/<int:emission_id>",
        view_func=emission_round_view.schedule_emission_round,
        methods=["POST"],
    )

    return emission_round_blueprint
