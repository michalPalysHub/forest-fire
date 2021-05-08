from flask import jsonify
from random import randint


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
