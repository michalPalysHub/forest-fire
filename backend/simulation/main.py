from time import time, sleep

from flask import jsonify

from .area import ForestArea
from .agents import *


class Simulation:
    """
    Wstępnie stąd będzie uruchamiana symulacja.
    """

    def __init__(self) -> None:
        """
        ...
        """
        # Rozmiary planszy.
        self.columns = 40
        self.rows = 20
        self.sector_size = 30

        # Minimalny czas jednego obiegu pętli [ms].
        self.min_loop_time = 750

        # Instancja klasy symbolizującej cały obszar lasu.
        self.forest_area = ForestArea(self.columns, self.rows, self.sector_size)

        # Instancje pojedynczych agentów biorących udział w symulacji.
        self.transfer = Transfer(self.forest_area)
        self.analyst = Analyst(self.forest_area)
        self.overseer = Overseer(self.forest_area)

        # Dane na temat czujników(???) oraz sektorów są przechowywane w słownikach.
        self.sensors = dict()
        self.sectors_data = dict()

        # Strażacy w liście.
        self.firefighters = list()

        # Flaga informująca o statusie uruchomienia symulacji.
        self.simulation_run = False

    def set_settings(self, settings: dict) -> None:
        """
        Konfiguracja symulacji na podstawie słownika settings.
        """
        # Rozmiary planszy.
        self.columns = settings.get('columns', self.columns)
        self.rows = settings.get('rows', self.rows)
        self.sector_size = settings.get('sector_size', self.sector_size)

        # Minimalny czas jednego obiegu pętli.
        self.min_loop_time = float(settings.get('newLoopTime', self.min_loop_time)) / 1000

    def set_init_data(self, data: dict) -> None:
        """
        Inicjalizacja symulacji po naciśnięciu przycisku 'Init'.
        """
        self.forest_area.init_area(data)
        self.forest_area.init_fire()
        self.transfer.sectors_data = dict.fromkeys(self.forest_area.sectors, 0)
        self.sensors = self.forest_area.init_sensors()

    def get_sectors_data(self) -> jsonify:
        """
        Zwraca JSON-a z aktualnymi informacjami na temat sektorów lasu.
        """
        self.sectors_data = self.transfer.get_sectors_data()

        return jsonify(sectors=self.sectors_data, simulation_run=self.simulation_run)

    def get_particular_sector_data(self, sector_id: int) -> jsonify:
        """
        Zwraca JSON-a z aktualnymi informacjami na temat danego sektora lasu.
        """
        return jsonify(self.sectors_data[sector_id])

    def reset(self) -> None:
        """
        Zatrzymanie symulacji oraz przywrócene ustawień początkowych.
        """
        self.__init__()
        self.simulation_run = False

    def stop(self) -> None:
        """
        Zatrzymanie symulacji na obecnym etapie - możliwe wznowienie.
        """
        self.simulation_run = False

    def run(self) -> None:
        """
        Główna funkcja zarządzająca symulacją. Po właczeniu działa dopóki zmianu statusu symulacji.
        """
        self.simulation_run = True

        while self.simulation_run:
            # Mierzony jest czas wykonania głównej pętli, żeby sprawdzić, czy nie wykonuje się zbyt długo.
            start = time()

            # Analityk aktualizuje ilośc palących się sektorów.
            self.analyst.update_number_of_sectors_on_fire()

            # Nadzorca wysyła straż pożarną na miejsca pożarów.
            self.firefighters = self.overseer.call_firefighters(self.analyst.on_fire_diff)

            # # Strażacy poruszają się w stronę ogniska pożaru gasząc ewentualne ogniska pożarów po drodze.
            for firefighter in self.firefighters.values():
                firefighter.move()

            # Aktualizacja pozycji strażaków na obszarze lasu. Ma to wpływ na rozprzestrzenianie się pożaru.
            self.forest_area.firefighters_locations = list(Firefighter.locations.values())

            # Funkcja odpowiedzialna za rozprzestrzenianie się ognia.
            self.forest_area.spread_fire()

            # Symulacja zatrzymuje się, jeżeli wszystkie sektory, które
            if not self.forest_area.forest_on_fire:
                self.simulation_run = False

            # Jeden obieg pętli powinien trwać co najmniej min_loop_time, które jest zdefiniowane przez użyktkownika.
            time_elapsed = time() - start
            if time_elapsed < self.min_loop_time:
                sleep(self.min_loop_time - time_elapsed)

            print(time_elapsed)

        print('Simulation done.')
