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

# Początkowe wartości CO2 w zależności od typu lasu [ppm].
CO2_START_VALUES = {
    1: 150,
    2: 175,
    3: 200
}

# Początkowa wartość PM2.5 [ug/m3].
PM25_START_VALUE = 25

# TODO: uzupełnić stałe o słownik z zależnościami ryzyk oraz stopni zaawansowania pożaru od wartości PM2.5 i CO2.