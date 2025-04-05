from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from inventory_app_container import InventoryAppContainer
from services.netcdf_blob_repository import NETCDFBlobRepository
from views.wrf_round_api import WRFRoundAPI


@inject
def register_wrf_round_api_routes(
    netcdf_blob_repository: NETCDFBlobRepository = Provide[
        InventoryAppContainer.netcdf_blob_repository
    ],
):
    wrf_round_api = WRFRoundAPI(netcdf_blob_repository)

    api_blueprint = Blueprint("wrf_round_api", __name__, url_prefix="/wrf_rounds_api")

    api_blueprint.add_url_rule(
        "/complete_the_round",
        view_func=wrf_round_api.complete_the_round,
        methods=["POST"],
    )

    return api_blueprint
