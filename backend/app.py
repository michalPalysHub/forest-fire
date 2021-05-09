from flask import Flask, request, jsonify

from simulation.main import Simulation
from simulation.area import COLUMNS, ROWS, SQUARE_SIZE


app = Flask(__name__)
simulation = Simulation()


@app.route('/dimensions', methods=['GET'])
def dimensions_set():
    dimensions_message = jsonify(message='Sent from Flask backend :)',
                      columns=COLUMNS,
                      rows=ROWS,
                      squareSize=SQUARE_SIZE)

    return dimensions_message


@app.route('/init_data', methods=['POST'])
def init_data_receive():
    init_squares_data = request.json
    simulation.set_init_data(init_squares_data)

    return init_squares_data


@app.route('/simulation', methods=['GET'])
def simulation_run():
    simulation_result = simulation.run()

    return simulation_result