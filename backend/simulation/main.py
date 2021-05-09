from flask import jsonify

from .area import ForestArea


class Simulation:
    """
    Wstępnie stąd będzie uruchamiana symulacja.
    """
    def __init__(self):
        """
        ...
        """
        # Instancje klas.
        self.forest_area = ForestArea()

    def set_init_data(self, data):
        self.forest_area.init_area(data)

    def get_data(self):
        """
        Tu wstępnie będzie generowany json z danymi na temat sektorow lasu.
        """
        forest_states = self.forest_area.get_forest_data()
        content = jsonify(forest_states=forest_states)

        return content
