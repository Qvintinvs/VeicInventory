from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from inventory_app_container import InventoryAppContainer
from repositories.netcdf_blob_repository import NETCDFBlobRepository
from views.netcdf_api_view import NETCDFAPIView


@inject
def create_netcdf_api_blueprint(
    netcdf_blob_repository: NETCDFBlobRepository = Provide[
        InventoryAppContainer.netcdf_blob_repository
    ],
):
    wrf_round_api = NETCDFAPIView(netcdf_blob_repository)

    api_blueprint = Blueprint("netcdf_api", __name__, url_prefix="/netcdf_api")

    api_blueprint.add_url_rule(
        "/submit_netcdf_file_for_round",
        view_func=wrf_round_api.complete_the_round,
        methods=["POST"],
    )

    return api_blueprint
