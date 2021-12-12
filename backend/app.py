from flask import Flask, request, jsonify

from simulation.main import Simulation

app = Flask(__name__)
simulation = Simulation()


@app.route('/dimensions', methods=['GET'])
def get_dimensions() -> jsonify:
    """
    Widok API zwracający aktualne wymiary planszy, tj. liczbę kolumn, wierszy oraz rozmiar sektora w
    sector_size x sector_size.
    """
    return jsonify(columns=simulation.columns, rows=simulation.rows, sectorSize=simulation.sector_size, status=200)


@app.route('/init_data', methods=['POST'])
def receive_init_data() -> jsonify:
    """
    Widok API odpowiedzialny za odbiór danych początkowych lasu, oraz inicjalizację symulacji na ich podstawie.
    """
    init_sectors_data = request.get_json()
    simulation.set_init_data(init_sectors_data)

    return jsonify(message='Init data received.', status=200)


@app.route('/start', methods=['POST'])
def run_simulation() -> jsonify:
    """
    Widok API odpowiedzialny uruchamiający symulację po otrzymaniu wiadomości.
    """
    simulation.run()

    return jsonify(message='Simulation started.', status=200)


@app.route('/reset', methods=['POST'])
def reset_data() -> jsonify:
    """
    Widok API odpowiedzialny za przywrócenie danych symulacji do stanu początkowego.
    """
    simulation.reset()

    return jsonify(messsage='Simulation reset done.', status=200)


@app.route('/stop', methods=['POST'])
def stop_simulation() -> jsonify:
    """
    Widok API zatrzymujący symulację na aktualnym etapie po otrzymaniu wiadomości.
    """
    simulation.stop()

    return jsonify(message='Simulation stopped.', status=200)


@app.route('/settings', methods=['POST'])
def set_settings() -> jsonify:
    """
    Widok API odpowiedzialny za odbieranie ustawień symulacji wybranych przez użytkownika, np. czasu pętli, lub
    zmienionych wymiarów planszy.
    """
    simulation.set_settings(request.get_json())

    return jsonify(message='Simulation settings reconfigured.', status=200)


@app.route('/sectors', methods=['GET'])
def get_sectors_data() -> jsonify:
    """
    Widok API przechowujący dane na temat wszystkich, zdefiniowanych sektorów.
    """
    sectors_data, simulation_run = simulation.get_sectors_data()

    return jsonify(sectors_data=sectors_data, simulation_run=simulation_run, status=200)


@app.route('/sectors/<int:uid>', methods=['GET'])
def get_particular_sector_data(uid: int) -> jsonify:
    """
    Widok API przechowujący dane na temat sektorze o identyfikatorze uid.
    """
    try:
        return jsonify(sector_data=simulation.sectors_data[uid], status=200)
    except KeyError:
        return jsonify(message='Sector with given ID does not exist!', status=404)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
