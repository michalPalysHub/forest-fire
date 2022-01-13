from __future__ import annotations

from time import time, sleep
from typing import Tuple
from threading import Thread

from .area import ForestArea
from .agents import *

from .helpers.csv_helper import CsvLogger
from .helpers.datetime import Datetime


class Simulation:
    """
    Wstępnie stąd będzie uruchamiana symulacja.
    """

    def __init__(self):
        """
        ...
        """
        # Rozmiary planszy.
        self.columns = 30
        self.rows = 20
        self.sector_size = 30

        # Instancja klasy odpowiedzialnej ze przechowywanie informacji o czasie.
        self.datetime = Datetime()

        # Minimalny czas jednego obiegu pętli [ms].
        self.min_loop_time = 1000

        # Instancja klasy symbolizującej cały obszar lasu.
        self.forest_area = ForestArea(self.columns, self.rows, self.sector_size)

        # Instancje pojedynczych agentów biorących udział w symulacji.
        self.transfer = Transfer(self.forest_area)
        self.analyst = Analyst(self.forest_area, self.datetime)
        self.overseer = Overseer(self.forest_area, self.datetime)

        # Dane na temat czujników(???) oraz sektorów są przechowywane w słownikach.
        self.sensors = dict()
        self.sectors_data = dict()

        # Instancja klasy słuzącej do logowania stanu wszystkich sektorów w trakcie pojedynczej symulacji
        self.csv_logger = CsvLogger(self.transfer, self.datetime)

        # Limit dostępnych wozów strażackich.
        self.firefighters_limit = 5

        # Strażacy w liście.
        self.firefighters = Firefighter.init_firefighters(self.firefighters_limit, self.forest_area, self.datetime)
        self.forest_area.update_firefighters_positions(self.firefighters)

        # Flaga informująca o statusie uruchomienia symulacji.
        self.simulation_run = False

        self.simulation_thread = None
        self.csv_logger_thread = None

    def set_settings(self, settings: dict):
        """
        Konfiguracja symulacji na podstawie słownika settings.
        """
        # Rozmiary planszy.
        self.columns = settings.get('columns', self.columns)
        self.rows = settings.get('rows', self.rows)
        self.sector_size = settings.get('sector_size', self.sector_size)

        # Ilość dostępnych wozów strażackich.
        self.firefighters_limit = int(settings.get('firefighters_limit', self.firefighters_limit))
        self.firefighters = Firefighter.init_firefighters(self.firefighters_limit, self.forest_area, self.datetime)
        self.forest_area.update_firefighters_positions(self.firefighters)

        # Minimalny czas jednego obiegu pętli.
        self.min_loop_time = int(settings.get('newLoopTime', self.min_loop_time))/1000

    def set_init_data(self, data: dict):
        """
        Inicjalizacja symulacji po naciśnięciu przycisku 'Init'.
        """
        self.forest_area.init_area(data)
        self.forest_area.init_fire()
        self.transfer.sectors_data = dict.fromkeys(self.forest_area.sectors, 0)
        self.sensors = self.forest_area.init_sensors()
        self.csv_logger.init_logging_process()

    def get_sectors_data(self) -> Tuple[dict, bool]:
        """
        Zwraca JSON-a z aktualnymi informacjami na temat sektorów lasu.
        """
        self.sectors_data = self.transfer.get_sectors_data()

        return self.sectors_data, self.simulation_run

    def get_particular_sector_data(self, sector_id: int) -> dict:
        """
        Zwraca JSON-a z aktualnymi informacjami na temat danego sektora lasu.
        """
        return self.sectors_data[sector_id]

    def reset(self):
        """
        Zatrzymanie symulacji oraz przywrócene ustawień początkowych.
        """
        self.csv_logger.is_logging = False
        self.simulation_run = False
        self.__init__()

    def start(self):
        """
        Uruchomienie symulacji - osobne wątki.
        """
        self.simulation_run = True
        self.csv_logger.start()
        if not self.simulation_thread:
            self.simulation_thread = Thread(target=self.run, args=(), daemon=True)
            self.simulation_thread.start()
        if not self.csv_logger_thread:
            self.csv_logger_thread = Thread(target=self.csv_logger.log_current_forest_area_state, args=(), daemon=True)
            self.csv_logger_thread.start()

    def stop(self):
        """
        Zatrzymanie symulacji na obecnym etapie - możliwe wznowienie.
        """
        self.simulation_run = False
        self.csv_logger.stop()
        self.simulation_thread = None
        self.csv_logger_thread = None

    def run(self):
        """
        Główna funkcja zarządzająca symulacją. Po właczeniu działa dopóki zmianu statusu symulacji.
        """
        while self.simulation_run:
            # Mierzony jest czas wykonania głównej pętli, żeby sprawdzić, czy nie wykonuje się zbyt długo.
            start = time()

            # Analityk aktualizuje ilośc palących się sektorów.
            self.analyst.update_number_of_sectors_on_fire()

            # Nadzorca wysyła straż pożarną na miejsca pożarów.
            self.firefighters = self.overseer.call_firefighters(self.analyst.on_fire_diff)

            # Strażacy poruszają się w stronę ogniska pożaru gasząc ewentualne ogniska pożarów po drodze.
            for firefighter in self.firefighters.values():
                firefighter.move()

            # Aktualizacja pozycji strażaków na obszarze lasu. Ma to wpływ na rozprzestrzenianie się pożaru.
            self.forest_area.update_firefighters_positions(self.firefighters)

            # Funkcja odpowiedzialna za rozprzestrzenianie się ognia.
            self.forest_area.spread_fire()

            # Symulacja zatrzymuje się, jeżeli wszystkie sektory, które
            if not self.forest_area.forest_on_fire:
                self.simulation_run = False

            # Jeden obieg pętli powinien trwać co najmniej min_loop_time, które jest zdefiniowane przez użyktkownika.
            time_elapsed = time() - start
            if time_elapsed < self.min_loop_time:
                sleep(self.min_loop_time - time_elapsed)

            self.datetime.move()

            print(time_elapsed)

        print('Simulation done.')
        self.stop()
