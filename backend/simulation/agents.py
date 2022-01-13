from __future__ import annotations

from .helpers.datetime import Datetime


class Sensor:
    SECTOR_SIZE = 5

    def __init__(self, uid, i, j):
        self.uid = uid
        self.i = i
        self.j = j

    def __repr__(self):
        return f'({self.i},{self.j})'


class Transfer:

    def __init__(self, forest_area):
        self.forest_area = forest_area
        self.sectors_data = dict()

    def get_sectors_data(self) -> dict:
        """
        Zwraca słownik sectors_data z aktualnymi parametrami każdego sektora lasu.
        """
        for sector_id in self.forest_area.sectors:
            sector = self.forest_area.sectors[sector_id]
            self.sectors_data[sector_id] = sector.get_data()

        return self.sectors_data


class Analyst:

    def __init__(self, forest_area, datetime: Datetime):
        self.forest_area = forest_area
        self.datetime = datetime
        self.num_of_on_fire = {'previous': 0, 'present': 0}
        self.on_fire_diff = int()

    def update_number_of_sectors_on_fire(self):
        self.num_of_on_fire['previous'] = self.num_of_on_fire['present']
        self.num_of_on_fire['present'] = len(self.forest_area.sectors_on_fire)
        self.on_fire_diff = self.num_of_on_fire['present'] - self.num_of_on_fire['previous']


class Overseer:

    def __init__(self, forest_area, datetime: Datetime):
        self.forest_area = forest_area
        self.datetime = datetime
        self.firefighters = dict()
        self.firefighters_called = list()

    def call_firefighters(self, on_fire_diff: int) -> dict:
        if on_fire_diff < 0:
            return self.firefighters

        while len(self.firefighters) < Firefighter.limit:
            for sector_id in self.forest_area.sectors_on_fire:
                if len(self.firefighters) == Firefighter.limit:
                    break
                sector = self.forest_area.sectors[sector_id]
                uid = len(self.firefighters)
                self.firefighters[uid] = Firefighter(uid, self.forest_area, self.datetime, sector_id, sector.i,
                                                     sector.j)
                self.firefighters_called.append(sector_id)

        return self.firefighters


class Patrol:

    def __init__(self):
        pass


class Firefighter:

    fire_departament_i = 10
    fire_departament_j = 20
    limit = 5
    day_move_speed = 1
    night_move_speed = 0.75
    night_hours = ['22:00', '6:00']

    def __init__(self,
            uid: int,
            forest_area,
            datetime: Datetime,
            order_sector_id: int = None,
            order_i: int = None,
            order_j: int = None
    ):
        self.forest_area = forest_area
        self.datetime = datetime
        self.id = uid
        self.i = self.fire_departament_i
        self.j = self.fire_departament_j
        self.sector_id = self.i * self.forest_area.columns + self.j
        self.order_sector_id = order_sector_id if order_sector_id is not None else self.sector_id
        self.order_i = order_i if order_i is not None else self.i
        self.order_j = order_j if order_j is not None else self.j
        self.forest_area.firefighters_positions[self.id] = self.sector_id
        self.fuel_increase = 15

    def __repr__(self) -> str:
        return str(self.id)

    def move(self):
        move_speed = self.__get_move_speed()
        self.get_order()

        self.__move_horizontally(move_speed)
        self.__move_vertically(move_speed)

        for neighbor_id in self.sector.neighbor_ids:
            self.forest_area.sectors[neighbor_id].can_spread = False

        self.forest_area.firefighters_positions[self.id] = self.sector_id

    def fight_fire(self):
        self.sector.firefighter_present = True
        self.sector.fuel += self.fuel_increase
        if self.sector.fuel >= 1000:
            self.sector.fuel = 1000
            self.sector.on_fire = False
            self.sector.state = 5
            self.sector.can_spread = False
            self.forest_area.sectors_on_fire.remove(self.sector_id)
            self.get_order()

    def get_order(self):
        if self.order_sector_id in self.forest_area.sectors_on_fire:
            return
        if self.forest_area.forest_on_fire:
            self.order_sector_id = self.get_closest_on_fire_sector()
            order_sector = self.forest_area.sectors[self.order_sector_id]
            self.order_i = order_sector.i
            self.order_j = order_sector.j

    def get_closest_on_fire_sector(self):
        min_distance = 1000
        uid = 0
        for sector_id in self.forest_area.sectors_on_fire:
            sector = self.forest_area.sectors[sector_id]
            i = sector.i
            j = sector.j
            distance = self.forest_area.get_distance(self.i, self.j, i, j)
            if distance < min_distance:
                min_distance = distance
                uid = sector.id

        return uid

    def __move_vertically(self, move_speed: float):
        if self.i > self.order_i:
            self.i -= move_speed
        elif self.i < self.order_i:
            self.i += move_speed
        self.sector_id = self.forest_area.get_id(self.i, self.j)
        self.__look_for_fire()

    def __move_horizontally(self, move_speed: float):
        if self.j > self.order_j:
            self.j -= move_speed
        elif self.j < self.order_j:
            self.j += move_speed
        self.sector_id = self.forest_area.get_id(self.i, self.j)
        self.__look_for_fire()

    def __look_for_fire(self):
        if self.sector_id in self.forest_area.sectors:
            self.sector = self.forest_area.sectors[self.sector_id]
            if self.sector_id in self.forest_area.sectors_on_fire:
                self.fight_fire()

    def __get_move_speed(self):
        night_start_dt = Datetime.from_string(self.night_hours[0])
        night_end_dt = Datetime.from_string(self.night_hours[1])
        move_speed = self.day_move_speed
        if self.datetime > night_start_dt or self.datetime < night_end_dt:
            move_speed = self.night_move_speed
        if self.i == self.order_i or self.j == self.order_j:
            if abs(self.i - self.order_i) > 1 or abs(self.j - self.order_j) > 1:
                move_speed *= 2

        return move_speed

    @classmethod
    def init_firefighters(cls, limit: int, forest_area, datetime: Datetime) -> dict[int, Firefighter]:
        cls.limit = limit
        return {i: Firefighter(i, forest_area, datetime) for i in range(limit)}
