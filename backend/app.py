from flask import Flask, request, jsonify

from simulation.main import Simulation

app = Flask(__name__)
simulation = Simulation()


@app.route('/dimensions', methods=['GET'])
def dimensions_set() -> jsonify:
    """
    Widok API zwracający aktualne wymiary planszy, tj. liczbę kolumn, wierszy oraz rozmiar sektora w
    sector_size x sector_size.
    """
    dimensions_message = jsonify(columns=simulation.columns, rows=simulation.rows, sectorSize=simulation.sector_size)

    return dimensions_message


@app.route('/init_data', methods=['POST'])
def init_data_receive() -> jsonify:
    """
    Widok API odpowiedzialny za odbiór danych początkowych lasu, oraz inicjalizację symulacji na ich podstawie.
    """
    init_sectors_data = request.json
    simulation.set_init_data(init_sectors_data)

    return 'Init data received.'


@app.route('/start', methods=['POST'])
def simulation_run() -> str:
    """
    Widok API odpowiedzialny uruchamiający symulację po otrzymaniu wiadomości.
    """
    simulation.run()

    return 'Simulation started.'


@app.route('/reset', methods=['POST'])
def reset_data() -> str:
    """
    Widok API odpowiedzialny za przywrócenie danych symulacji do stanu początkowego.
    """
    simulation.reset()

    return 'Simulation reset done.'


@app.route('/stop', methods=['POST'])
def stop_simulation() -> str:
    """
    Widok API zatrzymujący symulację na aktualnym etapie po otrzymaniu wiadomości.
    """
    simulation.stop()

    return 'Simulation paused.'


@app.route('/settings', methods=['POST'])
def settings() -> str:
    """
    Widok API odpowiedzialny za odbieranie ustawień symulacji wybranych przez użytkownika, np. czasu pętli, lub
    zmienionych wymiarów planszy.
    """
    simulation.set_settings(request.json)
    return 'Simulation settings reconfigured.'


@app.route('/sectors', methods=['GET'])
def sectors_data() -> jsonify:
    """
    Widok API przechowujący dane na temat wszystkich, zdefiniowanych sektorów.
    """
    return simulation.get_sectors_data()


@app.route('/sectors/<int:uid>', methods=['GET'])
def particular_sector_data(uid: int) -> jsonify or str:
    """
    Widok API przechowujący dane na temat sektorze o identyfikatorze uid.
    """
    try:
        return simulation.sectors_data[uid]
    except KeyError:
        return 'Sector with given ID does not exist!'


if __name__ == '__main__':
    app.run(debug=True)
