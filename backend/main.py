from flask import Flask, request

app = Flask(__name__)

COLUMNS = 40
ROWS = 20
SQUARE_SIZE = 30


@app.route('/send', methods=['GET'])
def send():
    return {
        'message': 'Sent from Flask backend :)',
        'columns': COLUMNS,
        'rows': ROWS,
        'squareSize': SQUARE_SIZE,
    }


@app.route('/receive', methods=['POST'])
def receive():
    message = request.json
    print(message)

    return message