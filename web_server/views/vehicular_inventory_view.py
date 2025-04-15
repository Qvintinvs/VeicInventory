from flask import redirect, render_template, url_for, send_file, request
from services.vehicles_repository import VehiclesRepository

from .vehicular_inventory_forms.vasques_vehicle_form import VasquesVehicleForm
from .vehicular_inventory_forms.vehicle_interactions_form import VehicleInteractionsForm


class VehicularInventoryView:
    def __init__(self, vehicular_inventory: VehiclesRepository):
        self.__inventory = vehicular_inventory

    def show_the_page(self):
        form: VasquesVehicleForm = VasquesVehicleForm()

        vehicle_dicts = self.__inventory.read_vehicles_data()
        print(f"vehicle_dicts: {vehicle_dicts}")

        return render_template("index.html", vehicular_data=vehicle_dicts, form=form)

    def send_new_vehicle(self):
        form: VasquesVehicleForm = VasquesVehicleForm()

        if form.validate_on_submit():
            vehicle_from_the_form = form.vehicle

            self.__inventory.insert_a(vehicle_from_the_form)

        return redirect(url_for("vehicular_inventory.show_the_page"))

    def send_id_to_delete(self):
        delete_form: VehicleInteractionsForm = VehicleInteractionsForm()

        if delete_form.validate_on_submit():
            id_to_delete = delete_form.action_id

            self.__inventory.delete_vehicle_by(id_to_delete)

        return redirect(url_for("vehicular_inventory.show_the_page"))

    def process(self):
        process_form: VehicleInteractionsForm = VehicleInteractionsForm()

        print(f"process_form: {process_form}")

        if process_form.validate_on_submit():
            id_to_process = process_form.action_id

            self.__inventory.send_vehicle_namelist_by(id_to_process)

        return redirect(url_for("vehicular_inventory.show_the_page"))
    
    def edit(self):
        form: VasquesVehicleForm = VasquesVehicleForm()
        form_withid: VehicleInteractionsForm = VehicleInteractionsForm()

        print(form.validate_on_submit())
        print(form_withid.validate_on_submit())

        if form.validate_on_submit() and form_withid.validate_on_submit():
            vehicle_from_the_form = form.vehicle
            action_id = form_withid.action_id
        
            print(f"vehicle_from_the_form: {vehicle_from_the_form}")
            self.__inventory.edit(vehicle_from_the_form.to_dict(), its_id=action_id)
            print(f"form_withid: {form_withid.action_id}")

        return redirect(url_for("vehicular_inventory.show_the_page"))
    
    def visualize(self):
        # process_form: VehicleInteractionsForm = VehicleInteractionsForm()

        # if process_form.validate_on_submit():
            # self.__inventory.visualize(id)
        # return "0"
        return render_template("render_plot.html")
    
    # test
    def get_netcdf_data(self, data_variable: str = None, altitude:int = None):
        data_variable = request.args.get('data_variable')
        if not data_variable:
            data_variable = "CO2_BIO"

        altitude = request.args.get('altitude', type=int)
        if not altitude:
            altitude = 0

        from flask import jsonify
        import numpy as np
        from netCDF4 import Dataset

        nc_file_path = "D:/Users/Public/Documents/arquivos/Trabalhos/College/IFSC/Projeto de Pesquisa WRF/wrf stuff/web-ui wrf/VeicInventory/test/wrfout"
        dataset = Dataset(nc_file_path, mode="r")


        # Extract latitudes and longitudes
        # lats = dataset.variables["XLAT"][0, :, :]  # Assuming 3D and selecting the first time slice
        # lons = dataset.variables["XLONG"][0, :, :]  # Assuming 3D and selecting the first time slice

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
        target_vars = [var for var in variable_names if len(dataset.variables[var].dimensions) == 4]
        variable = dataset.variables[data_variable] 

        # Print attributes (before slicing!)
        # print(f"Attributes for variable '{data_variable}':")
        # for attr in variable.ncattrs():
        #     print(f"{attr}: {getattr(variable, attr)}")

        description = getattr(variable, 'description', 'N/A')
        units = getattr(variable, 'units', 'N/A')
        
        variable_values = variable[:]  # Convert to NumPy array
        # print(f"target_vars: {target_vars}")

        # Handle MaskedArrays for CO2_ANT
        if isinstance(variable_values, np.ma.MaskedArray):
            variable_values = variable_values.filled(np.nan)  # Replace masked values with NaN

        # Create frames for CO2_ANT
        variable_frames = []
        for t in range(variable_values.shape[0]):  # Iterate over the time dimension
            variable_frames.append(variable_values[t, altitude, :, :].tolist())  # Assuming bottom_top=0 for simplicity



        # Close the dataset
        dataset.close()

        # Prepare and return JSON response
        return jsonify({
            "lats": lats.tolist(),
            "lons": lons.tolist(),
            "time": times.tolist(),  # Match variable name to the JS code
            "frames": variable_frames,
            "target_vars": target_vars,
            "description": description,
            "units": units,
        })

