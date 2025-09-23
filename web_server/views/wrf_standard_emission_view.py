from flask import flash, redirect, render_template, request, url_for
from forms.wrf_standard_emission_form import WRFStandardEmissionForm
from repositories.wrf_standard_emission_repository import WRFStandardEmissionRepository
from repositories.wrfchemi_blobs import MinioRepository


class WRFStandardEmissionView:
    def __init__(
        self,
        vehicle_emissions_repository: WRFStandardEmissionRepository,
        wrfchemi_blobs_repository: MinioRepository,
    ):
        self.__inventory = vehicle_emissions_repository
        self.__wrfchemi = wrfchemi_blobs_repository

    def render_inventory_page(self):
        vehicle_emissions = self.__inventory.list_emissions()

        return render_template(
            "index.html",
            emission_data=vehicle_emissions,
            form=WRFStandardEmissionForm(),
        )

    def add_vehicle_emission(self):
        vasques_form: WRFStandardEmissionForm = WRFStandardEmissionForm()

        if vasques_form.validate_on_submit():
            vehicle_form_data = vasques_form.vehicle

            self.__inventory.save_vehicle_emission(vehicle_form_data)

        return redirect(url_for("wrf_standard.render_inventory_page"))

    def delete_vehicle_emission(self, emission_id: int):
        # TODO: return a status value that will be passed to the template
        try:
            self.__inventory.delete_data_by_id(emission_id)
        except Exception:
            flash(f"Emission with ID {emission_id} not found.", "error")

        return redirect(url_for("wrf_standard.render_inventory_page"))

    # TODO: move this method to a dedicated class
    def visualize(self):
        return render_template("render_plot.html")

    # TODO: move this method to a dedicated class, same as visualize
    def get_netcdf_data(
        self, data_variable: str | None = None, altitude: int | None = None
    ):
        data_variable = request.args.get("data_variable")
        if not data_variable:
            data_variable = "CO2_BIO"

        altitude = request.args.get("altitude", type=int)
        if not altitude:
            altitude = 0

        import numpy as np
        from flask import jsonify
        from netCDF4 import Dataset

        nc_file_path = "D:/Users/Public/Documents/arquivos/Trabalhos/College/IFSC/Projeto de Pesquisa WRF/wrf stuff/web-ui wrf/VeicInventory/test/wrfout"
        dataset = Dataset(nc_file_path, mode="r")

        # Extract latitudes and longitudes
        # lats = dataset.variables["XLAT"][0, :, :]  # Assuming 3D and selecting the first time slice
        # lons = dataset.variables["XLONG"][0, :, :]  # Assuming 3D and selecting the first time slice
        alts = dataset.variables["XLAT"][:, 0, 0]
        alts_length = alts.size
        # print(f"alts_length: {alts_length}")
        # alts_length = 0

        lats = dataset.variables["XLAT"][altitude, :, :]
        lons = dataset.variables["XLONG"][altitude, :, :]

        # Handle MaskedArrays
        if isinstance(lats, np.ma.MaskedArray):
            lats = lats.filled(np.nan)  # Replace masked values with NaN
        if isinstance(lons, np.ma.MaskedArray):
            lons = lons.filled(np.nan)  # Replace masked values with NaN

        # Extract time and CO2_ANT data
        times = dataset.variables["XTIME"][:]  # Assuming time is not masked

        # Get all variable names
        variable_names = dataset.variables.keys()

        # Filter the ones containing XTIME, XLAT, and XLONG
        target_vars = [
            var for var in variable_names if len(dataset.variables[var].dimensions) == 4
        ]
        variable = dataset.variables[data_variable]

        # Print attributes (before slicing!)
        # print(f"Attributes for variable '{data_variable}':")
        # for attr in variable.ncattrs():
        #     print(f"{attr}: {getattr(variable, attr)}")

        description = getattr(variable, "description", "N/A")
        units = getattr(variable, "units", "N/A")

        variable_values = variable[:]  # Convert to NumPy array
        # print(f"target_vars: {target_vars}")

        zmin = float(np.nanmin(variable_values))
        zmax = float(np.nanmax(variable_values))

        # Handle MaskedArrays for CO2_ANT
        if isinstance(variable_values, np.ma.MaskedArray):
            variable_values = variable_values.filled(
                np.nan
            )  # Replace masked values with NaN

        # Create frames for CO2_ANT
        variable_frames = []
        for t in range(variable_values.shape[0]):  # Iterate over the time dimension
            variable_frames.append(
                variable_values[t, altitude, :, :].tolist()
            )  # Assuming bottom_top=0 for simplicity

        # Close the dataset
        dataset.close()

        # Prepare and return JSON response
        return jsonify(
            {
                "lats": lats.tolist(),
                "lons": lons.tolist(),
                "time": times.tolist(),  # Match variable name to the JS code
                "frames": variable_frames,
                "target_vars": target_vars,
                "description": description,
                "units": units,
                "zmin": zmin,
                "zmax": zmax,
                "alts_length": alts_length,
            }
        )
