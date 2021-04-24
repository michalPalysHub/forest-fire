from flask import Flask

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def api():
    return {
        'message': 'Sent from Flask backend :)',
        'columns': 20,
        'rows': 20,
        'area_width': 600,
        'area_height': 600,
    }
