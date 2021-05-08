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
    0: 'NONE',      # Brak lasu
    1: 'DECIDOUS',  # Las liściasty
    2: 'MIXED',     # Las mieszany
    3: 'CONIFEROUS' # Las iglasty
}


class ForestArea:
    def __init__(self):
        pass


class ForestSquare:
    def __init__(self, i, j, forest_type):
        """
        Każdy obszar symbolizujący jeden, najmniejszy sektor lasu posiada atrybuty takie jak:
            - współrzędne i, j na planszy;
            - typ lasu;
            - parametry przedstawione w dokumentacji (temperatura, wilgotność powietrza, etc.);
            - stan lasu:
                - 1:5 - zagrożenia pożarem;
                - 6:8 - stopień zaawansowania pożaru;
                - 9 - spalony sektor.
        """
        self.i = i
        self.j = j
        self.forest_type = forest_type

        self.temperature = float()
        self.air_humidity = float()
        self.litter_moisture = float() # Wilgotność ściółki.
        self.wind_speed = float()
        self.wind_directory = str()

        self.state = int()
