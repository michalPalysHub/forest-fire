from flask import jsonify
from random import randint

# Do testów.
COLUMNS = 40
ROWS = 20
SQUARE_SIZE = 30


class Simulation:
    """
    Wstępnie stąd będzie uruchamiana symulacja.
    """
    def __init__(self):
        pass

    def get_data(self):
        forest_states = [[randint(1, 8) for _ in range(COLUMNS)] for _ in range(ROWS)]
        content = jsonify(forest_states=forest_states)

        return content

        # TODO: z tego co zauważyłem, to każde pobranie z API danych powoduje odświeżenie api view (kto by pomyślał XD)
        # więc może to na froncie powinno się odbywać cykliczne wywoływanie GetDataFromApi? Np. każdorazowe uruchomienie
        # GetDataFromApi wywołuje na backendzie funkcje pchającą symulację do przodu i zwracającą jsona na view.
