from flask import abort, redirect, render_template, url_for
from forms.wrf_standard_emission_form import WRFStandardEmissionForm
from repositories.vasques_round_query_repository import WRFStandardRoundQueryRepository
from repositories.wrf_round_command_repository import WRFRoundCommandRepository


class WRFStandardRoundView:
    def __init__(
        self,
        vehicle_emissions_repository: WRFStandardRoundQueryRepository,
        wrf_round_command_repository: WRFRoundCommandRepository,
        wrfchemi_blobs_repository,
    ):
        self.__inventory = vehicle_emissions_repository
        self.__rounds = wrf_round_command_repository
        self.__wrfchemi_repo = wrfchemi_blobs_repository

    def render_emission_selection_page(self):
        vehicle_emissions = self.__inventory.list_emissions()

        return render_template(
            "index.html",
            emission_data=vehicle_emissions,
            form=WRFStandardEmissionForm(),
        )

    def dispatch_round_execution(self, round_id: int):
        emission_round = self.__inventory.get_round_by_id(round_id)

        if emission_round is None:
            abort(404, description=f"No emission found for ID {round_id}")

        self.__rounds.publish_pending_round(emission_round)

        return redirect(url_for("emission_round.render_emission_selection_page"))

    def schedule_emission_round(self, emission_id: int):
        emission_round = self.__inventory.generate_round_from_emission(emission_id)

        if emission_round is None:
            abort(404, description=f"No emission found for ID {emission_id}")

        self.__rounds.save_emission_round(emission_round)

        return self.dispatch_round_execution(emission_round.id)
