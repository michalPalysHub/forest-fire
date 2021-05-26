from time import time, sleep
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
        # Rozmiary planszy.
        self.columns = 40
        self.rows = 20
        self.sector_size = 30

        # Minimalny czas jednego obiegu pętli.
        self.min_loop_time = 750

        # Instancje klas.
        self.forest_area = ForestArea(self.columns, self.rows, self.sector_size)
        self.sensors = dict()   # W lesie mamy kilka czujników, objekty przechowywane są w słowniku.
        self.sectors_data = dict()

        self.simulation_run = False

    def set_settings(self, settings):
        # Rozmiary planszy.
        self.columns = settings.get('columns', self.columns)
        self.rows = settings.get('rows', self.rows)
        self.sector_size = settings.get('sector_size', self.sector_size)

        # Minimalny czas jednego obiegu pętli.
        self.min_loop_time = float(settings.get('newLoopTime', self.min_loop_time))/1000

    def set_init_data(self, data):
        """
        Inicjalizacja symulacji po naciśnięciu przycisku 'Init'.
        """
        self.__init__()
        self.forest_area.init_area(data)
        self.forest_area.init_fire()
        self.sensors = self.forest_area.init_sensors()
        self.sectors_data = self.forest_area.get_sectors_data()

    def get_sectors_data(self):
        """
        Zwraca JSON-a z aktualnymi informacjami na temat sektorów lasu.
        """
        self.sectors_data = self.forest_area.get_sectors_data()

        return jsonify(sectors=self.sectors_data, simulation_run=self.simulation_run)

    def get_particular_sector_data(self, sector_id):
        """
        Zwraca JSON-a z aktualnymi informacjami na temat danego sektora lasu.
        """
        return jsonify(self.sectors_data[sector_id])

    def reset(self):
        self.simulation_run = False
        self.__init__()

    def reset(self):
        self.simulation_run = False

    def run(self):
        self.simulation_run = True
        while self.simulation_run:
            start = time()
            self.forest_area.spread_fire()
            time_elapsed = time() - start
            if time_elapsed < self.min_loop_time:
                sleep(self.min_loop_time - time_elapsed)
            if self.forest_area.whole_forest_burned:
                self.simulation_run = False
            print(time_elapsed)

        print('Simulation done.')
