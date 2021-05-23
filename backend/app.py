from flask import Flask, request, jsonify

from simulation.main import Simulation
from simulation.constants import COLUMNS, ROWS, SECTOR_SIZE

app = Flask(__name__)
simulation = Simulation()


@app.route('/dimensions', methods=['GET'])
def dimensions_set():
    dimensions_message = jsonify(columns=COLUMNS,
                                 rows=ROWS,
                                 sectorSize=SECTOR_SIZE)

    return dimensions_message


@app.route('/init_data', methods=['POST'])
def init_data_receive():
    init_sectors_data = request.json
    simulation.set_init_data(init_sectors_data)

    return init_sectors_data


@app.route('/sectors', methods=['GET'])
def sectors_data():
    return simulation.get_sectors_data()


@app.route('/sectors/<int:uid>', methods=['GET'])
def particular_sector_data(uid):
    try:
        return simulation.forest_data[uid]
    except KeyError:
        return 'Sector with given ID does not exist!'


@app.route('/simulation', methods=['GET'])
def simulation_run():
    return simulation.run()
