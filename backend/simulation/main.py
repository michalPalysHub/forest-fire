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

    def set_init_data(self, data):
        """
        Ustalenie stanów początkowych na podstawie zaakceptowanego formatu lasu po kliknięciu przycisku 'Start'.
        """
        self.forest_area.init_area(data)
        self.analyst.prepare_buf(data)
        self.sensors = self.forest_area.get_sensors()

    def run(self):
        """
        Głowna funkcja zarządzająca symulacją. Zwraca JSON-a z zaktualizowanymi informacjami na temat sektorów lasu.
        """
        forest_states = self.forest_area.get_forest_data()
        content = jsonify(forest_states)

        return content
