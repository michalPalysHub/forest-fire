from flask import Flask, request

app = Flask(__name__)

COLUMNS = 20
ROWS = 20
AREA_WIDTH = 600
AREA_HEIGHT = 600


@app.route('/send', methods=['GET'])
def send():
    return {
        'message': 'Sent from Flask backend :)',
        'columns': COLUMNS,
        'rows': ROWS,
        'area_width': AREA_WIDTH,
        'area_height': AREA_HEIGHT,
    }


@app.route('/receive', methods=['POST'])
def receive():
    message = request.json
    print(message)

    return message