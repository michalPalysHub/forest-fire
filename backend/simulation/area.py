from pprint import pprint

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

FOREST_TYPES = {
    0: 'NONE',  # Brak lasu
    1: 'DECIDOUS',  # Las liściasty
    2: 'MIXED',  # Las mieszany
    3: 'CONIFEROUS'  # Las iglasty
}


class ForestArea:
    def __init__(self):
        self.area = dict()
        self.forest_data = list()

    def init_area(self, init_data):
        self.prepare_forest_data_list(len(init_data))
        for square_id in init_data:
            square = init_data[square_id]
            i = square['i']
            j = square['j']
            forest_type = square['forestType']
            self.area[square_id] = ForestSquare(square_id, i, j, forest_type)

    def prepare_forest_data_list(self, length):
        self.forest_data = {str(square_id): {} for square_id in range(length)}

    def get_forest_data(self):
        for square_id in self.area:
            square = self.area[square_id]
            self.forest_data[square_id] = square.get_square_data()

        return self.forest_data


class ForestSquare:
    def __init__(self, square_id, i, j, forest_type):
        """
        Każdy obszar symbolizujący jeden, najmniejszy sektor lasu posiada atrybuty takie jak:
            - unikalne id sektora;
            - współrzędne i, j na planszy;
            - typ lasu;
            - parametry przedstawione w dokumentacji (temperatura, wilgotność powietrza, etc.);
            - stan lasu:
                - 1:5 - zagrożenia pożarem;
                - 6:8 - stopień zaawansowania pożaru;
                - 9 - spalony sektor.
        """
        self.id = square_id
        self.i = i
        self.j = j
        self.forest_type = forest_type

        self.temperature = float()
        self.air_humidity = float()
        self.litter_moisture = float()  # Wilgotność ściółki.
        self.wind_speed = float()
        self.wind_directory = str()

        self.state = int()

        self.square_data = dict()

    def __repr__(self):
        return f'({self.i},{self.j})'

    def get_square_data(self):
        self.square_data = {'id': self.id,
                            'i': self.i,
                            'j': self.j,
                            'forest_type': self.forest_type,
                            'temperature': self.temperature,
                            'air_humidity': self.air_humidity,
                            'litter_moisture': self.litter_moisture,
                            'wind_speed': self.wind_speed,
                            'wind_directory': self.wind_directory,
                            'state': self.state}

        return self.square_data
