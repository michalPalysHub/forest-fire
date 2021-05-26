<<<<<<< HEAD
from random import randint, uniform
from math import ceil

from .agents import SensorAgent
from .constants import COLUMNS, ROWS, CO2_START_VALUES, PM25_START_VALUE
=======
import random

from math import ceil, log, exp, sqrt

from .agents import SensorAgent
from .constants import *
>>>>>>> f0b11df (Integrated backend with front changes.)


class ForestArea:
    """
    Symbolizuje las jako cały obszar. Zawiera informacje na temat struktury lasu, tj. rozkładu kwadratów
    reprezentujących sektor lasu oraz ułożenia czujników.
    """
<<<<<<< HEAD
    def __init__(self):
=======
    def __init__(self, columns, rows, sector_size):
>>>>>>> f0b11df (Integrated backend with front changes.)
        """
<<<<<<< HEAD
        squares - słownik zawierający instancje sektorów lasu;
        squares_data - słownik zawierający informacje na temat poszczególnych kwadratów lasu;
        sensors - słownik zawierający instancje czujników.
        """
        self.squares = dict()
        self.squares_data = dict()
        self.sensors= dict()
=======
        sectors - słownik zawierający instancje sektorów lasu;
        sensors - słownik zawierający instancje czujników;
        sectors_on_fire - słownik id kwadratów objętych pożarem na początku wraz z z stopniami zaawansowania.
        """
        self.columns = columns
        self.rows = rows
        self.sector_size = sector_size

        self.sectors = dict()
        self.sensors = dict()
        self.sectors_on_fire = list()
>>>>>>> 2732a73 (squares -> sectors)

        self.fire_initted = False
        self.whole_forest_burned = False

    def init_area(self, init_data):
        """
        Aktualizacja danych na temat sektorów lasu na podstawie informacji uzyskanych od front-u po zatwierdzeniu
        początkowych parametrów lasu.
        """
        self.prepare_sector_buffors(init_data)
        for sector_id in self.sectors:
            sector = init_data[str(sector_id)]
            i = sector['i']
            j = sector['j']
            forest_type = sector['forestType']
            self.sectors[sector_id] = ForestSector(sector_id, i, j, forest_type)
            self.sectors[sector_id].neighbor_ids = self.get_direct_neighbor_ids(i, j)

    def prepare_sector_buffors(self, data):
        """
        Przygotowanie słownika z polem na dane dla każdego sektora planszy pod warunkiem, że został oznaczony jako las.
        """
        self.sectors = {int(uid): {} for uid in data if data[uid]['forestType'] != 0}
        print(self.sectors)

<<<<<<< HEAD
<<<<<<< HEAD
    def get_forest_data(self):
=======
    def init_fire(self, amount=3):
>>>>>>> 2732a73 (squares -> sectors)
=======
    def init_fire(self, amount=5):
>>>>>>> f0b11df (Integrated backend with front changes.)
        """
        Zwraca słownik squares_data z aktualnymi parametrami każdego sektora lasu.
        """
<<<<<<< HEAD
<<<<<<< HEAD
        for square_id in self.squares:
            square = self.squares[square_id]
            self.squares_data[square_id] = square.get_square_data()

        return self.squares_data
=======
        # self.sectors_on_fire = [random.choice(list(self.sectors.keys())) for _ in range(amount)]
        self.sectors_on_fire = [82]
        for sector_id in self.sectors_on_fire:
            sector = self.sectors[sector_id]
            sector.set_on_fire()
            self.update_neighborhood(sector)
>>>>>>> 2732a73 (squares -> sectors)
=======
        amount = random.randint(3, 6)
        self.sectors_on_fire = [random.choice(list(self.sectors.keys())) for _ in range(amount)]
        # self.sectors_on_fire = [54, 234, 345, 566, 735]
        for sector_id in self.sectors_on_fire:
            sector = self.sectors[sector_id]
            sector.set_on_fire()

        self.fire_initted = True
>>>>>>> f0b11df (Integrated backend with front changes.)

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

<<<<<<< HEAD
        for i in range(start_i, ROWS, sector_size):
            for j in range(start_j, COLUMNS, sector_size):
=======
        for i in range(start, self.rows, sector_size):
            for j in range(start, self.columns, sector_size):
>>>>>>> f0b11df (Integrated backend with front changes.)
                uid += 1
                self.sensors[uid] = SensorAgent(uid, i, j)

        return self.sensors

<<<<<<< HEAD
<<<<<<< HEAD
=======
    def get_forest_data(self):
=======
    def get_sectors_data(self):
>>>>>>> f0b11df (Integrated backend with front changes.)
        """
        Zwraca słownik sectors_data z aktualnymi parametrami każdego sektora lasu.
        """
        sectors_data = dict()
        for sector_id in self.sectors:
            sector = self.sectors[sector_id]
            sectors_data[sector_id] = sector.get_data()

        return sectors_data

    def update_neighborhood(self, center):
        """
        Aktualizacja parametrów pogodowych na podstawie zmian w sektorze 'center'. Z założenia funkcja ta ma służyć
        do uwzględnienia wpływu pożaru wewnątrz jednego sektora na cały las. Przykładowo, gdy na skutek pożaru
        temperatura wewnątrz jednego sektoru wzrośnie, temperatura na okolicznych sektorach także powinna wzrosnąć.
        """
        center_data = center.get_changeable_weather_data()

<<<<<<< HEAD
=======
        if not self.fire_initted:
            sector_ids = self.sectors
        else:
            # sector_ids = center.neighbor_ids
            sector_ids = self.get_direct_neighbor_ids(center.i, center.j, int(center.state/2))

        for sector_id in sector_ids:
            if sector_id != center.id:
                if sector_id not in self.sectors_on_fire:
                    sector = self.sectors[sector_id]
                    distance = self.get_distance(center.i, center.j, sector.i, sector.j)
                    data = sector.get_changeable_weather_data()
                    for parameter, value in data.copy().items():
                        data[parameter] = self.get_updated_parameter(parameter, value, center_data[parameter], distance, center.state)
                    sector.update_data(data)

    def get_direct_neighbor_ids(self, i, j, distance=1):
        neigbhor_ids = list()
        for m in range(i - distance, i + distance + 1):
            for n in range(j - distance, j + distance + 1):
                if (m, n) != (i, j):
                    uid = self.get_id(m, n)
                    if uid in self.sectors and uid not in self.sectors_on_fire:
                        neigbhor_ids.append(uid)

        return neigbhor_ids

>>>>>>> f0b11df (Integrated backend with front changes.)
    @staticmethod
    def get_distance(i1, j1, i2, j2):
        """
        Wyznaczenie odległości w sektorach między sektorem 1 -> (i1, j1), oraz sektorem drugim -> (i2, j2)
        """
        return sqrt((i1 - i2) ** 2 + (j1 - j2) ** 2)

    @staticmethod
    def get_updated_parameter(name, present, center, distance, max_distance):
        """
        Wyznaczenie nowej wartości parametru pogodowego na podstawie jego typu, wartości obecnej, wartości na sektorze,
        porównawczym oraz odległości między nimi.
        """
        if distance <= max_distance:
            if name in ['temperature', 'co2', 'pm25']:
                return round(present + ((center - present) * (max_distance - distance) / max_distance), 2)
            elif name in ['air_humidity', 'litter_moisture']:
                return round(present - ((present - center) * (max_distance - distance) / max_distance), 2)
        else:
            return present

    def get_id(self, i, j):
        """
        Wyznaczenie ID sektora na podstawie jego współrzędnych.
        """
        if (0 <= i < 40) and (0 <= j < 40):
            return i * self.columns + j
        else:
            return None

    def spread_fire(self):
        """
        Funkcja odpowiedzialna za progresywne rozprzestrzenianie się pożaru. Nwm, czy będzie potrzebna.
        """
        for sector_id in self.sectors_on_fire.copy():
            sector = self.sectors[sector_id]
            self.update_sector_due_fire(sector)
            neighbor_ids = sector.neighbor_ids
            for neighbor_id in neighbor_ids:
                self.set_neighbors_on_fire(neighbor_id, sector)
        self.check_if_whole_forest_burned()

    def update_sector_due_fire(self, sector):
        sector.update_cause_of_fire()
        self.update_neighborhood(sector)
        if sector.state == 9:
            self.sectors_on_fire.remove(sector.id)
            sector.burned = True

    def set_neighbors_on_fire(self, uid, sector_on_fire):
        neighbor = self.sectors[uid]
        if not (neighbor.on_fire or neighbor.burned):
            prob = [True, False]
            if neighbor.i < sector_on_fire.i:
                prob.extend([True,True, False])
            if neighbor.j > sector_on_fire.j:
                prob.append([True,True, False])
            if random.choice(prob):
                self.sectors_on_fire.append(uid)
                neighbor.on_fire = True
                neighbor.state = random.randint(6, sector_on_fire.state)
                self.update_neighborhood(neighbor)

    def check_if_whole_forest_burned(self):
        if len(self.sectors_on_fire) == 0:
            self.whole_forest_burned = True

>>>>>>> 2732a73 (squares -> sectors)

class ForestSector:
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

        self.temperature = 28 + round(uniform(-2,2), 1) # Temperatura powietrza [°C].
        self.air_humidity = 13 + round(uniform(-3,3), 1) # Wilgtoność powietrza [%].
        self.litter_moisture = 8 + round(uniform(-3,3), 1) # Wilgotność ściółki [%].
        self.wind_speed = 8 + round(uniform(-1,1), 1) # Prędkość wiatru  [km/h].
        self.wind_directory = 'NE'
        self.co2_value = CO2_START_VALUES[self.forest_type] + round(uniform(-5,5), 1) # Wartość stężenia CO2 [ppm].
        self.pm25_value = PM25_START_VALUE + round(uniform(-2, 2), 1) # Wartość stężenia PM2.5 [ug/m3].

<<<<<<< HEAD
        self.square_state = randint(1,8)

        self.square_data = dict()
=======
        self.on_fire = False
        self.burned = False
        self.counter = 0
        self.ffdi = float()
        self.k = K_FACTORS[self.forest_type]
        self.state = int()

        self.neighbor_ids = list()
        self.data = dict()
>>>>>>> f0b11df (Integrated backend with front changes.)

        self.update_risk_info()

    def __repr__(self):
        """
        Zmiana formy wyświetlania objektu, np. w tablicy.
        """
        return f'({self.i},{self.j})'

    def get_square_data(self):
        """
        Pozyskanie aktualnych parametrów danego sektoru.
        """
<<<<<<< HEAD
        self.square_data = {'id': self.uid,
                            'i': self.i,
                            'j': self.j,
                            'forest_type': self.forest_type,
                            'temperature': self.temperature,
                            'air_humidity': self.air_humidity,
                            'litter_moisture': self.litter_moisture,
                            'wind_speed': self.wind_speed,
                            'wind_directory': self.wind_directory,
                            'co2_value': self.co2_value,
                            'pm25_value': self.pm25_value,
                            'square_state': self.square_state,
                            }
=======
        self.data = {
            'i': self.i,
            'j': self.j,
            'forest_type': self.forest_type,
            'temperature': self.temperature,
            'air_humidity': self.air_humidity,
            'litter_moisture': self.litter_moisture,
            'wind_speed': self.wind_speed,
            'wind_directory': self.wind_directory,
            'co2': self.co2,
            'pm25': self.pm25,
            'sector_state': self.state,
            'ffdi': self.ffdi,
            'on_fire': self.on_fire
        }
>>>>>>> 2732a73 (squares -> sectors)

        return self.square_data

    def update_square_data(self, **kwargs):
        """
        Aktualizacja parametrów danego sektoru na skutek uruchomionej symulacji.
        """
<<<<<<< HEAD
        self.temperature = kwargs['temperature']
        self.air_humidity = kwargs['humidity']
        self.litter_moisture = kwargs['litter_moisture']
        self.wind_speed = kwargs['wind_speed']
        self.wind_directory = kwargs['wind_directory']
        self.co2_value = kwargs['co2_value']
        self.pm25_value = kwargs['pm25_value']
        self.square_state = kwargs['square_state']
=======
        self.temperature = data.get('temperature', self.temperature)
        self.air_humidity = data.get('air_humidity', self.air_humidity)
        self.litter_moisture = data.get('litter_moisture', self.litter_moisture)
        self.wind_speed = data.get('wind_speed', self.wind_speed)
        self.wind_directory = data.get('wind_directory', self.wind_directory)
        self.co2 = data.get('co2_value', self.co2)
        self.pm25 = data.get('pm25_value', self.pm25)
        self.update_risk_info()

    def update_cause_of_fire(self):
        self.counter += 1
        if self.counter == 3 and self.state <= 9:
            self.counter = 0
            self.state += 1

        self.temperature += self.state/10
        self.air_humidity -= 1/self.state
        self.litter_moisture -= 1/self.state
        self.co2 += 10 * self.state
        self.pm25 += 4 * self.state
        self.update_risk_info()

    def update_risk_info(self):
        """
        Aktualizacja informacji mówiących o zagrożeniu pożarem.
        """
        self.update_ffdi()
        if not self.on_fire:
            self.update_state()

    def update_ffdi(self):
        """
        Aktualizacja współczynnika FFDI.
        """
        self.ffdi = round(
            self.k * 2 * exp(-0.45 + 0.987 * log(10 * (100 - self.litter_moisture) / 100) - 0.0345 *
                                  self.air_humidity + 0.0338 * self.temperature + 0.0234 * self.wind_speed), 2)
>>>>>>> f0b11df (Integrated backend with front changes.)

