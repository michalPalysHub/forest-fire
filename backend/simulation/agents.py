"""
Nie jestem do końca pewien, czy to w ogóle będzie potrzebne. :_)
"""

class SensorAgent:
    SECTOR_SIZE = 5

    def __init__(self, uid, i, j):
        self.uid = uid
        self.i = i
        self.j = j

    def __repr__(self):
        return f'({self.i},{self.j})'


class TransferAgent:
    def __init__(self):
        pass


class AnalystAgent:
    def __init__(self):
        self.ffdis = dict()

    def prepare_buf(self, data):
        self.ffdis = {square_id: None for square_id in data}


class OverseerAgent:
    def __init__(self):
        pass


class PatrolAgent:
    def __init__(self):
        pass


class FirefighterAgent:
    def __init__(self):
        pass