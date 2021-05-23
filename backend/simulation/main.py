from flask import jsonify

from .area import ForestArea
from .agents import *


class Simulation:
    """
    Wstępnie stąd będzie uruchamiana symulacja.
    """
    def __init__(self):
        """
        ...
        """
        # Instancje klas.
        self.forest_area = ForestArea()
        self.analyst = AnalystAgent()
        self.sensors = dict()   # W lesie mamy kilka czujników, objekty przechowywane są w słowniku.

        self.forest_data = dict()

    def set_init_data(self, data):
        """
        Ustalenie stanów początkowych na podstawie zaakceptowanego formatu lasu po kliknięciu przycisku 'Start'.
        """
        self.forest_area.init_area(data)
<<<<<<< HEAD
        self.analyst.prepare_buf(data)
        self.sensors = self.forest_area.get_sensors()
=======
        self.forest_area.init_fire()
        self.sensors = self.forest_area.init_sensors()
        self.forest_data = self.forest_area.get_forest_data()

    def get_sectors_data(self):
        """
        Zwraca JSON-a z aktualnymi informacjami na temat sektorów lasu.
        """
        return jsonify(self.forest_data)

    def get_particular_sector_data(self, sector_id):
        """
        Zwraca JSON-a z aktualnymi informacjami na temat danego sektora lasu.
        """
        return jsonify(self.forest_data[sector_id])
>>>>>>> 2732a73 (squares -> sectors)

    def run(self):
        """
        Głowna funkcja zarządzająca symulacją. Zwraca JSON-a z zaktualizowanymi informacjami na temat sektorów lasu.
        """
<<<<<<< HEAD
        forest_states = self.forest_area.get_forest_data()
        content = jsonify(forest_states)
=======
        self.forest_data = self.forest_area.get_forest_data()
        self.forest_area.spread_fire()
>>>>>>> 2732a73 (squares -> sectors)

        return jsonify(self.forest_data)
