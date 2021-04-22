from flask import Flask

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def api():
    return {
        'message': 'Sent from Flask backend :)',
        'columns': 10,
        'rows': 10,
        'area_height': 800,
        'area_width': 800,
    }
