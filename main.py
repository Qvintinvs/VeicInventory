from flask import Flask, render_template, request, jsonify
import numpy as np
from netCDF4 import Dataset
import f90nml
import os
import paramiko
from dotenv import load_dotenv

nml_params = ['frac_veic1','use_veic1','co_e_veic1','co2_e_veic1','ch4_e_veic1','frac_veic2','use_veic2','co_e_veic2','co2_e_veic2','ch4_e_veic2','frac_veic3','use_veic3','co_e_veic3','co2_e_veic3','ch4_e_veic3','frac_veic4a','use_veic4a','co_e_veic4a','co2_e_veic4a','ch4_e_veic4a','frac_veic4b','use_veic4b','co_e_veic4b','co2_e_veic4b','ch4_e_veic4b','frac_veic4c','use_veic4c','co_e_veic4c','co2_e_veic4c','ch4_e_veic4c','frac_veic5','use_veic5','co_e_veic5','co2_e_veic5','ch4_e_veic5','frac_veic6','use_veic6','co_e_veic6','co2_e_veic6','ch4_e_veic6']

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', params=nml_params)
    
    if request.method == 'POST':
        # field1 = request.args.get("field1")
        # field2 = request.args.get("field2")

        data = request.form

        # print(field1)
        # print(field2)
        print(data)

        data = request.form.to_dict()
        for key, value in data.items():
            if value.strip():
                data[key] = float(value)
            else:
                data[key] = 0


        namelist_group = {'emission_vehicles': data}

        with open('namelist.emis', 'w') as nml_file:
            f90nml.write(namelist_group, nml_file)

    return '''
    <script>
    alert("dados recebidos com sucesso")
    window.location.replace("/")
    </script>'''

@app.route("/sendfile", methods=['GET'])
def send_file():

    load_dotenv()

    hostname = os.getenv("SSH_HOST")
    username = os.getenv("SSH_NAME")
    password = os.getenv("SSH_PASS")
    local_file_path = os.getenv("LOCAL_FILE")
    remote_file_path = os.getenv("REMOTE_PATH")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)

    sftp = client.open_sftp()
    sftp.put(local_file_path, remote_file_path)

    stdin, stdout, stderr = client.exec_command("cd /dados3/CURSO/grupo1/test; ls")

    output = stdout.read().decode()

    print(output)

    return output

@app.route("/get_netcdf_data", methods=['GET'])
def get_netcdf_data():
    from flask import jsonify
    import numpy as np
    from netCDF4 import Dataset

    nc_file_path = "test/wrfout"
    dataset = Dataset(nc_file_path, mode="r")

    # Extract latitudes and longitudes
    lats = dataset.variables["XLAT"][0, :, :]  # Assuming 3D and selecting the first time slice
    lons = dataset.variables["XLONG"][0, :, :]  # Assuming 3D and selecting the first time slice

    # Handle MaskedArrays
    if isinstance(lats, np.ma.MaskedArray):
        lats = lats.filled(np.nan)  # Replace masked values with NaN
    if isinstance(lons, np.ma.MaskedArray):
        lons = lons.filled(np.nan)  # Replace masked values with NaN

    # Extract time and CO2_ANT data
    times = dataset.variables["XTIME"][:]  # Assuming time is not masked
    co2_ant = np.array(dataset.variables["CO2_ANT"][:])  # Convert to NumPy array

    # Handle MaskedArrays for CO2_ANT
    if isinstance(co2_ant, np.ma.MaskedArray):
        co2_ant = co2_ant.filled(np.nan)  # Replace masked values with NaN

    # Create frames for CO2_ANT
    co2_ant_frames = []
    for t in range(co2_ant.shape[0]):  # Iterate over the time dimension
        co2_ant_frames.append(co2_ant[t, 0, :, :].tolist())  # Assuming bottom_top=0 for simplicity

    # Close the dataset
    dataset.close()

    # Prepare and return JSON response
    return jsonify({
        "lats": lats.tolist(),
        "lons": lons.tolist(),
        "time": times.tolist(),  # Match variable name to the JS code
        "frames": co2_ant_frames
    })


@app.route("/render_results", methods=['GET'])
def render_results():
    return render_template("render_plot.html")

app.run(debug=True)
