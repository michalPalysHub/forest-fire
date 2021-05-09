from random import randint, uniform
from math import ceil

from .agents import SensorAgent

# Rozmiary planszy.
COLUMNS = 40
ROWS = 20
SQUARE_SIZE = 30

# Kierunki wiatru, tak o wypisane.
WIND_DIRECTORIES = {
    1: 'N',
    2: 'NE',
    3: 'E',
    4: 'SE',
    5: 'S',
    6: 'SW',
    7: 'W',
    8: 'NW'
}

# Typy lasu - tak jak wyżej.
FOREST_TYPES = {
    0: 'NONE',  # Brak lasu
    1: 'DECIDOUS',  # Las liściasty
    2: 'MIXED',  # Las mieszany
    3: 'CONIFEROUS'  # Las iglasty
}


class ForestArea:
    """
    Symbolizuje las jako cały obszar. Zawiera informacje na temat struktury lasu, tj. rozkładu kwadratów
    reprezentujących sektor lasu oraz ułożenia czujników.
    """
    def __init__(self):
        """
        squares - słownik zawierający instancje sektorów lasu;
        squares_data - słownik zawierający informacje na temat poszczególnych kwadratów lasu;
        sensors - słownik zawierający instancje czujników.
        """
        self.squares = dict()
        self.squares_data = dict()
        self.sensors= dict()

    def init_area(self, init_data):
        """
        Aktualizacja danych na temat sektorów lasu na podstawie informacji uzyskanych od front-u po zatwierdzeniu
        początkowych parametrów lasu.
        """
        self.prepare_squares_dict(init_data)
        for square_id in self.squares:
            square = init_data[square_id]
            i = square['i']
            j = square['j']
            forest_type = square['forestType']
            self.squares[square_id] = ForestSquare(square_id, i, j, forest_type)

    def prepare_squares_dict(self, data):
        """
        Przygotowanie słownika z polem na dane dla każdego sektora planszy pod warunkiem, że został oznaczony jako las.
        """
        self.squares = {uid: {} for uid in data if data[uid]['forestType'] != 0}

    def get_forest_data(self):
        """
        Zwraca słownik squares_data z aktualnymi parametrami każdego sektora lasu.
        """
        for square_id in self.squares:
            square = self.squares[square_id]
            self.squares_data[square_id] = square.get_square_data()

        return self.squares_data

    def get_sensors(self):
        """
        Rozstawienie czujników na planszy. Czujniki są wstawiane od określonego przez ustalony sektor czujnika pola.
        Przykładowo dla rozmiaru sektoru równego 5 obszar obejmowany przez czujnik to 5x5 kwadratów. Zatem Początkowa
        pozycja czujnika to i=3, j=3.
        """
        sector_size = SensorAgent.SECTOR_SIZE
        start_i = ceil(sector_size/2)-1
        start_j = start_i
        uid = 0

        for i in range(start_i, ROWS, sector_size):
            for j in range(start_j, COLUMNS, sector_size):
                uid += 1
                self.sensors[str(uid)] = SensorAgent(uid, i, j)

        return self.sensors


class ForestSquare:
    """
    Zawiera informacje na temat poszczególnych, niejmniejszych sektorów lasu.
    """
    def __init__(self, uid, i, j, forest_type):
        """
        Każdy sektor posiada atrybuty takie jak:
            - unikalne id sektora;
            - współrzędne i, j na planszy;
            - typ lasu;
            - parametry przedstawione w dokumentacji (temperatura, wilgotność powietrza, etc.) - aktualnie zamockowane;
            - stan lasu:
                - 1:5 - zagrożenia pożarem;
                - 6:8 - stopień zaawansowania pożaru;
                - 9 - spalony sektor.
        """
        self.uid = uid
        self.i = i
        self.j = j
        self.forest_type = forest_type

        self.temperature = 28 + round(uniform(-2,2), 1)
        self.air_humidity = 13 + round(uniform(-3,3), 1)
        self.litter_moisture = 8 + round(uniform(-3,3), 1) # Wilgotność ściółki.
        self.wind_speed = 8 + round(uniform(-1,1), 1) # Prędkość wiatru w km/h.
        self.wind_directory = 'NE'

        self.square_state = randint(1,8)

        self.square_data = dict()

    def __repr__(self):
        """
        Zmiana formy wyświetlania objektu, np. w tablicy.
        """
        return f'({self.i},{self.j})'

    def get_square_data(self):
        """
        Pozyskanie aktualnych parametrów danego sektoru.
        """
        self.square_data = {'id': self.uid,
                            'i': self.i,
                            'j': self.j,
                            'forest_type': self.forest_type,
                            'temperature': self.temperature,
                            'air_humidity': self.air_humidity,
                            'litter_moisture': self.litter_moisture,
                            'wind_speed': self.wind_speed,
                            'wind_directory': self.wind_directory,
                            'square_state': self.square_state}

        return self.square_data

    def update_square_data(self, temperature, humidity, litter_moisture, wind_speed, wind_directory, square_state):
        """
        Aktualizacja parametrów danego sektoru na skutek uruchomionej symulacji.
        """
        self.temperature = temperature
        self.air_humidity = humidity
        self.litter_moisture = litter_moisture
        self.wind_speed = wind_speed
        self.wind_directory = wind_directory
        self.square_state = square_state

