from flask import Flask, request, jsonify

from simulation.main import Simulation


app = Flask(__name__)
simulation = Simulation()

COLUMNS = 40
ROWS = 20
SQUARE_SIZE = 30


@app.route('/dimensions', methods=['GET'])
def dimensions_set():
    content = jsonify(message='Sent from Flask backend :)',
                      columns=COLUMNS,
                      rows=ROWS,
                      squareSize=SQUARE_SIZE)

    return content


@app.route('/init_data', methods=['POST'])
def init_data_receive():
    squares_data = request.json
    simulation.set_init_data(squares_data)

    return squares_data


@app.route('/simulation', methods=['GET'])
def simulation_run():
    content = simulation.get_data()

    return content