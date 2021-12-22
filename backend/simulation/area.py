from __future__ import annotations

import random

from math import ceil, sqrt, log, exp, pi

from .agents import Sensor
from .constants import CO2_START_VALUES, PM25_START_VALUE, K_FACTORS, CHANGEABLE_PARAMETERS, WIND_DIRECTIONS


class ForestArea:
    """
    Symbolizuje las jako cały obszar. Zawiera informacje na temat struktury lasu, tj. rozkładu kwadratów
    reprezentujących sektor lasu oraz ułożenia czujników.
    """

    def __init__(self, columns: int, rows: int, sector_size: int):
        """
        Inicjalizacja instancji klasy ForestArea. Pobiera wymiary planszy oraz deklaruje wymagane kontenery na dane oraz
        flagi.
        """
        self.columns = columns
        self.rows = rows
        self.sector_size = sector_size

        self.sectors = dict()
        self.sensors = dict()
        self.sectors_on_fire = list()

        self.fire_initted = False
        self.forest_on_fire = False
        self.firefighters_locations = list()

    def init_area(self, init_data: dict):
        """
        Inicjalizacja danych na temat sektorów lasu na podstawie informacji uzyskanych od front-u po zatwierdzeniu
        początkowych parametrów lasu.
        """
        self.prepare_sector_buffors(init_data)
        for sector_id in self.sectors:
            sector = init_data[str(sector_id)]
            i = sector['i']
            j = sector['j']
            forest_type = sector['forestType']
            is_fire_source = sector['isFireSource']
            self.sectors[sector_id] = ForestSector( sector_id, i, j, forest_type, is_fire_source)
            self.sectors[sector_id].neighbor_ids = self.get_direct_neighbor_ids(i, j)

    def prepare_sector_buffors(self, data: dict):
        """
        Przygotowanie słownika z polem na dane dla każdego sektora planszy pod warunkiem, że został oznaczony jako las.
        """
        self.sectors = {int(uid): {} for uid in data if data[uid]['forestType'] != 0}

    def init_fire(self):
        """
        Wywołanie pożaru na kilku sektorach lasu na początku symulacji, oraz aktualizacja na tej podstawie sektorów
        sąsiednich. Docelowo sektory, na których będzie wywoływany pożar będą zaznaczane przez użytkownika.
        """
        for sector_id in self.sectors:
            sector = self.sectors[sector_id]
            if sector.is_fire_source:
                self.sectors_on_fire.append(sector_id)
                sector.set_on_fire()

        self.fire_initted = True

    def init_sensors(self) -> dict:
        """
        Rozstawienie czujników na planszy. Czujniki są wstawiane od określonego przez ustalony sektor czujnika pola.
        Przykładowo dla rozmiaru sektoru równego 5 obszar obejmowany przez czujnik to 5x5 kwadratów. Zatem Początkowa
        pozycja czujnika to i=3, j=3.
        """
        # tbh to bezsens, żeby tak to robić, do usuniecia pewnie
        sector_size = Sensor.SECTOR_SIZE
        start = ceil(sector_size / 2) - 1
        uid = 0

        for i in range(start, self.rows, sector_size):
            for j in range(start, self.columns, sector_size):
                uid += 1
                self.sensors[uid] = Sensor(uid, i, j)

        return self.sensors

    def update_neighborhood(self, center: ForestSector):
        """
        Aktualizacja parametrów pogodowych na podstawie zmian w sektorze 'center'. Z założenia funkcja ta ma służyć
        do uwzględnienia wpływu pożaru wewnątrz jednego sektora na cały las. Przykładowo, gdy na skutek pożaru
        temperatura wewnątrz jednego sektoru wzrośnie, temperatura na okolicznych sektorach także powinna wzrosnąć.
        """
        # Pobranie aktualnych wartości parametrów pogodowych ulegających zmianie podczas pożaru.
        center_data = center.get_changeable_weather_data()

        # Jeżeli pożar nie został zainicjowany pod uwagę jest brany cały las. Jeżeli został zainicjowany pod uwagę
        # brane jest kilka sektorów wokół badanego, w zależności od jego stanu.
        if not self.fire_initted:
            sector_ids = self.sectors
        else:
            sector_ids = self.get_direct_neighbor_ids(center.i, center.j, int(center.state / 2))

        # Aktualizacja parametrów pogodowych dla każdego sektora poza badanym z sector_ids, w zalezności od odległości
        # do sektora badanego.
        for sector_id in sector_ids:
            if sector_id != center.id:
                if sector_id not in self.sectors_on_fire:
                    sector = self.sectors[sector_id]
                    distance = self.get_distance(center.i, center.j, sector.i, sector.j)
                    data = sector.get_changeable_weather_data()
                    for parameter, value in data.copy().items():
                        data[parameter] = self.get_updated_parameter(parameter, value, center_data[parameter], distance,
                                                                     center.state)
                    sector.update_data(data)

    def get_direct_neighbor_ids(self, i: int, j: int, radius: int = 1) -> list:
        """
        Zwraca listę identyfikatorów sektorów, znajdujących się w promieniu distance od sektora o współrzędnych (i, j).
        """
        neigbhor_ids = list()
        for m in range(i - radius, i + radius + 1):
            for n in range(j - radius, j + radius + 1):
                if self.get_distance(i, j, m, n) <= radius:
                    if (m, n) != (i, j):
                        uid = self.get_id(m, n)
                        if uid in self.sectors and uid not in self.sectors_on_fire:
                            neigbhor_ids.append(uid)

        return neigbhor_ids

    @staticmethod
    def get_distance(i1: int, j1: int, i2: int, j2: int) -> float:
        """
        Wyznaczenie odległości w sektorach między sektorem 1 -> (i1, j1), oraz sektorem drugim -> (i2, j2)
        """
        return sqrt((i1 - i2) ** 2 + (j1 - j2) ** 2)

    @staticmethod
    def get_updated_parameter(name: str, present: float, center: float, distance: float, max_distance: int) -> float:
        """
        Wyznaczenie nowej wartości parametru pogodowego na podstawie jego typu, wartości obecnej, wartości na sektorze,
        porównawczym, odległości między nimi oraz maksymalnej, wpływającej na daną wartość odległości.
        """
        if distance <= max_distance:
            if name in ['temperature', 'co2', 'pm25']:
                return round(present + ((center - present) * (max_distance - distance) / max_distance), 2)
            elif name in ['air_humidity', 'litter_moisture']:
                return round(present - ((present - center) * (max_distance - distance) / max_distance), 2)
        else:
            return present

    def get_id(self, i: int, j: int) -> int or None:
        """
        Wyznaczenie ID sektora na podstawie jego współrzędnych.
        """
        if (0 <= i < self.columns) and (0 <= j < self.columns):
            return i * self.columns + j
        else:
            return None

    def update_sector_due_fire(self, sector: ForestSector):
        """
        Aktualizuje parametry danego sektoru na skutek trwającego pożaru. Uwzględnia także wpływ pożaru na sektory
        sąsiednie.
        """
        sector.update_cause_of_fire()
        self.update_neighborhood(sector)
        if sector.burned:
            self.sectors_on_fire.remove(sector.id)

    def set_neighbors_on_fire(self, uid: int, sector_on_fire: ForestSector):
        """
        Funkcja odpowiedzialna za rozchodzenie się pożaru z jednego sektora na sąsiednie, nie objęte pożarem ani
        niespalone.
        """
        neighbor = self.sectors[uid]
        if not (neighbor.on_fire or neighbor.burned):
            if neighbor.id not in self.firefighters_locations:
                prob = self.get_spread_probability(sector_on_fire, neighbor)
                if random.random() <= prob:
                    self.sectors_on_fire.append(uid)
                    neighbor.on_fire = True
                    neighbor.state = random.randint(6, sector_on_fire.state)
                    self.update_neighborhood(neighbor)

    def get_spread_probability(self, sector_on_fire, neighbor):
        divider = 2500
        prob = float(neighbor.ffdi/divider)
        wind_direction = sector_on_fire.wind_direction
        diff_horizontal = sector_on_fire.j - neighbor.j
        diff_vertical = sector_on_fire.i - neighbor.i

        if diff_horizontal > 0:
            if wind_direction == 'W':
                prob += float(neighbor.wind_speed/divider)
            elif wind_direction in ['SW', 'NW']:
                prob += float(neighbor.wind_speed/2*divider)
        elif diff_horizontal < 0:
            if wind_direction == 'E':
                prob += float(neighbor.wind_speed/divider)
            elif wind_direction in ['SE', 'NE']:
                prob += float(neighbor.wind_speed/2*divider)

        if diff_vertical > 0:
            if wind_direction == 'N':
                prob += float(neighbor.wind_speed/divider)
            elif wind_direction in ['NE', 'NW']:
                prob += float(neighbor.wind_speed/2*divider)
        elif diff_vertical < 0:
            if wind_direction == 'S':
                prob += float(neighbor.wind_speed/divider)
            elif wind_direction in ['SE', 'SW']:
                prob += float(neighbor.wind_speed/2*divider)

        return prob

    def is_forest_on_fire(self):
        """
        Funkcja odpowiedzialna za sprawdzenie, czy pożar został ugaszony lub cały las zostal spalony.
        """
        if len(self.sectors_on_fire) == 0:
            self.forest_on_fire = False
        else:
            self.forest_on_fire = True

    def spread_fire(self):
        """
        Funkcja odpowiedzialna za progresywne rozprzestrzenianie się pożaru.
        """
        for sector_id in self.sectors_on_fire.copy():
            sector = self.sectors[sector_id]
            self.update_sector_due_fire(sector)
            neighbor_ids = sector.neighbor_ids
            if sector.can_spread:
                for neighbor_id in neighbor_ids:
                    if neighbor_id not in self.firefighters_locations:
                        self.set_neighbors_on_fire(neighbor_id, sector)
        self.is_forest_on_fire()


class ForestSector:
    """
    Zawiera informacje na temat poszczególnych, niejmniejszych sektorów lasu.
    """
    def __init__(self, uid: int, i: int, j: int, forest_type: int, is_fire_source: bool):
        """
        Inicjalizacja sektora lasu. Deklaruje informacje o położeniu, typie lasu, warunkach pogodowych, flagi
        informujące o stanie pożaru oraz inne kontenery na dane.
        """
        self.id = uid
        self.i = i
        self.j = j
        self.forest_type = forest_type
        self.is_fire_source = is_fire_source

        # Temperatura powietrza [°C].
        self.temperature = 28 + round(random.uniform(-2, 2), 1)
        # Wilgtoność powietrza [%].
        self.air_humidity = 13 + round(random.uniform(-3, 3), 1)
        # Wilgotność ściółki [%].
        self.litter_moisture = 16 + round(random.uniform(-3, 3), 1)
        # Prędkość wiatru [km/h].
        self.wind_speed = 8 + round(random.uniform(-1, 1), 1)
        # Kierunek wiatru.
        self.wind_direction = random.choice(WIND_DIRECTIONS)
        # Wartość stężenia CO2 [ppm].
        self.co2 = CO2_START_VALUES[self.forest_type] + round(random.uniform(-5, 5), 1)
        # Wartość stężenia PM2.5 [ug/m3].
        self.pm25 = PM25_START_VALUE + round(random.uniform(-2, 2), 1)

        self.fuel = 1000
        self.on_fire = False
        self.burned = False
        self.can_spread = False
        self.firefighter_present = False
        self.counter = 0
        self.ffdi = float()
        self.k = K_FACTORS[self.forest_type]
        self.state = int()

        self.neighbor_ids = list()
        self.data = dict()

        self.update_risk_info()

    def __repr__(self) -> str:
        """
        Zmiana formy wyświetlania objektu, np. w tablicy.
        """
        return str(self.id)

    def set_on_fire(self):
        """
        Inicjacja pożaru na danym sektorze. Skutkuje to zmianą wartości parametrów pogodowych.
        """
        self.state = random.randint(6, 8)
        self.on_fire = True
        self.reduce_fuel()

        self.temperature = 30 + round(random.uniform(0, self.state ** 2 / 10), 1)
        self.air_humidity = 5 + round(random.uniform(0, self.state ** 2 / 10), 1)
        self.litter_moisture = 5 + round(random.uniform(0, self.state ** 2 / 10), 1)
        self.co2 = 1.5 * CO2_START_VALUES[self.forest_type] + round(random.uniform((self.state - 1) ** 2 / 2,
                                                                                   self.state ** 2 / 2), 1)
        self.pm25 = round(random.uniform(self.state - 1, self.state) / 2 * PM25_START_VALUE, 1)
        self.update_ffdi()

    def get_data(self) -> dict:
        """
        Pozyskanie wszystkich, aktualnych informacji na temat danego sektoru. Realizowane na potrzeby widoku API.
        """
        self.data = {
            'i': self.i,
            'j': self.j,
            'forest_type': self.forest_type,
            'is_fire_source': self.is_fire_source,
            'temperature': round(self.temperature, 2),
            'air_humidity': round(self.air_humidity, 2),
            'litter_moisture': round(self.litter_moisture, 2),
            'wind_speed': round(self.wind_speed, 1),
            'wind_directory': self.wind_direction,
            'co2': round(self.co2, 1),
            'pm25': round(self.pm25, 1),
            'sector_state': self.state,
            'ffdi': round(self.ffdi, 2),
            'on_fire': self.on_fire
        }

        return self.data

    def get_changeable_weather_data(self) -> dict:
        """
        Uzyskanie wartości parametrów pogodowych, które zmieniają się podczas pożaru.
        """
        data = self.get_data()
        weather_data = {parameter: data[parameter] for parameter in data if parameter in CHANGEABLE_PARAMETERS}

        return weather_data

    def update_data(self, data: dict):
        """
        Aktualizacja parametrów danego sektoru na skutek uruchomionej symulacji.
        """
        self.temperature = data.get('temperature', self.temperature)
        self.air_humidity = data.get('air_humidity', self.air_humidity)
        self.litter_moisture = data.get('litter_moisture', self.litter_moisture)
        self.wind_speed = data.get('wind_speed', self.wind_speed)
        self.wind_direction = data.get('wind_directory', self.wind_direction)
        self.co2 = data.get('co2', self.co2)
        self.pm25 = data.get('pm25', self.pm25)
        self.update_risk_info()

    def update_cause_of_fire(self):
        """
        Aktualizacja parametrów stanu sektora oraz parametrów pogodowych na skutek pożaru. Counter zlicza wywołania tej
        funkcji, i jeżeli osiągnie zadeklarowaną wartość zwiększa stan ryzyka lub zagrożenia.
        """
        self.reduce_fuel()

        self.temperature = self.temperature + self.state / 10 if self.temperature < 70 else 70 +  random.random()
        self.air_humidity = self.air_humidity - 1 / self.state if self.air_humidity > 2 else 2 - 0.5 * random.random()
        self.litter_moisture = self.litter_moisture - 1 / self.state if self.litter_moisture > 2 \
            else 2 - 0.5 * random.random()
        self.co2 = self.co2 + 10 * self.state if self.co2 < 8000 else 8000 + 50 * random.random()
        self.pm25 = self.pm25 + self.state if self.pm25 < 500 else 500 + 10 * random.random()
        self.update_risk_info()

    def reduce_fuel(self):
        self.fuel -= self.ffdi * self.state / 20

    def update_risk_info(self):
        """
        Aktualizacja informacji mówiących o zagrożeniu pożarem.
        """
        self.update_ffdi()
        if self.on_fire and not self.burned:
            self.update_state_due_fire()
        elif not self.on_fire and not self.burned:
            self.update_state_due_risk()

    def update_ffdi(self):
        """
        Aktualizacja współczynnika FFDI.
        """
        self.ffdi = round(
            self.k * 2 * exp(-0.45 + 0.987 * log(10 * (100 - self.litter_moisture) / 100) - 0.0345 *
                             self.air_humidity + 0.0338 * self.temperature + 0.0234 * self.wind_speed), 2)

    def update_state_due_risk(self):
        """
        Wyznaczenie stanu pożarowego na danym sektorze, na podstawie współczynnika FFDI.
        """
        if self.ffdi < 5:
            self.state = 1
        elif 5 <= self.ffdi < 12:
            self.state = 2
        elif 12 <= self.ffdi < 24:
            self.state = 3
        elif 24 <= self.ffdi < 50:
            self.state = 4
        elif self.ffdi >= 50:
            self.state = 5

    def update_state_due_fire(self):
        if self.fuel <= 800 and not self.firefighter_present:
            self.can_spread = True

        if self.state == 6 and self.fuel <= 600:
            self.state = 7
        elif self.state == 7 and self.fuel <= 300:
            self.state = 8
        elif self.state == 8 and self.fuel <= 0:
            self.fuel = 0
            self.state = 9
            self.burned = True
            self.on_fire = False
