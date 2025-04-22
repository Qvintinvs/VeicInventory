from flask import Blueprint
from views.wrf_round_api import WRFRoundAPI


def create_wrf_round_api_blueprint():
    wrf_round_api = WRFRoundAPI()

    _ = wrf_round_api

    api_blueprint = Blueprint("wrf_round_api", __name__, url_prefix="/wrf_rounds_api")

    return api_blueprint
