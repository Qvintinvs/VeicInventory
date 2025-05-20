import redis
from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from inventory_app_container import InventoryAppContainer
from services.vasques_emission_round_repository import VasquesEmissionRoundRepository
from views.round_processing import RoundProcessing


@inject
def create_round_processing_blueprint(
    vasques_emission_round_repository: VasquesEmissionRoundRepository = Provide[
        InventoryAppContainer.vasques_emission_round_repository
    ],
    redis_client: redis.Redis = Provide[InventoryAppContainer.redis_client],
):
    rounds_view = RoundProcessing(vasques_emission_round_repository, redis_client)

    rounds_blueprint = Blueprint("round_processing", __name__, url_prefix="/round")

    rounds_blueprint.add_url_rule(
        "/process", view_func=rounds_view.process, methods=["POST"]
    )

    return rounds_blueprint
