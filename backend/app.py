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


@app.route('/simulation', methods=['GET'])
def simulation_run():
    content = simulation.get_data()

    return content


@app.route('/receive', methods=['POST'])
def data_receive():
    message = request.json
    print(message)

    return message

# dla każdego kwadratu i, j, foresttype
# 1-8, 1-5 ryzyka, 6-8 zagrożenia
# 1-8, 1-5 ryzyka, 6-8 zagrożenia