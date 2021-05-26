from flask import Flask, request, jsonify
from simulation import constants

from simulation.main import Simulation

app = Flask(__name__)
simulation = Simulation()


@app.route('/dimensions', methods=['GET'])
def dimensions_set():
    dimensions_message = jsonify(columns=simulation.columns,
                                 rows=simulation.rows,
                                 sectorSize=simulation.sector_size)

    return dimensions_message


@app.route('/init_data', methods=['POST'])
def init_data_receive():
    init_sectors_data = request.json
    simulation.set_init_data(init_sectors_data)

    return 'Init data receive.'


@app.route('/start', methods=['POST'])
def simulation_run():
    simulation.run()

    return 'Simulation started.'


@app.route('/reset', methods=['POST'])
def reset_data():
    simulation.reset()

    return 'Simulation reset done.'

@app.route('/pause', methods=['POST'])
def pause_simulation():
    simulation.pause()

    return 'Simulation paused.'


@app.route('/settings/looptime', methods=['POST'])
def settings():
    simulation.set_settings(request.json)
    return 'Simulation settings reconfigured.'


@app.route('/sectors', methods=['GET'])
def sectors_data():
    return simulation.get_sectors_data()


@app.route('/sectors/<int:uid>', methods=['GET'])
def particular_sector_data(uid):
    try:
        return simulation.sectors_data[uid]
    except KeyError:
        return 'Sector with given ID does not exist!'

if __name__ == '__main__':
    app.run(debug=True)
