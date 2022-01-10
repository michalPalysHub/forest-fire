from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from copy import deepcopy

from datetime import datetime


@dataclass(order=True)
class Datetime:
    day: Optional[int] = None
    month: Optional[int] = None
    year: Optional[int] = None
    hour: Optional[int] = None
    minute: Optional[int] = None

    def __post_init__(self):
        day, month, year, hour, minute = self.__get_current_datetime_splitted()
        self.day = self.day if self.day is not None else day
        self.month = self.month if self.month is not None else month
        self.year = self.year if self.year is not None else year
        self.hour = self.hour if self.hour is not None else hour
        self.minute = self.minute if self.minute is not None else minute
        self.factor_to_change = None
        self.interval = 1  # In minutes for now.

    def __repr__(self):
        return f'{self.hour:02d}:{self.minute:02d} {self.day:02d}.{self.month:02d}.{self.year}'

    def __sub__(self, other: Datetime) -> int:
        if self.hour < other.hour:
            return (self.hour - other.hour + 24) * 60 + self.minute - other.minute
        return (self.hour - other.hour) * 60 + self.minute - other.minute

    def move(self):
        self.minute += self.interval
        self.synchronize()

    def synchronize(self):
        while True:
            self.__synchronize_minute()
            self.__synchronize_hour()
            self.__synchronize_day()
            self.__synchronize_month()
            self.__synchronize_year()
            if self.minute < 60:
                break

    @staticmethod
    def from_string(_time: str) -> Datetime:
        time_splitted = _time.split(':')
        if len(time_splitted) == 1:
            hour = int(time_splitted[-1])
            minute = 0
        elif len(time_splitted) == 2:
            hour, minute = map(int, time_splitted)
        else:
            raise ValueError('Provided invalid format for period for one of more residents! It should be hh:mm!')

        return Datetime(hour=hour, minute=minute)

    def copy(self):
        return deepcopy(self)

    def __synchronize_minute(self):
        if self.minute >= 60:
            self.minute -= 60
            self.factor_to_change = 'hour'
        else:
            self.factor_to_change = None

    def __synchronize_hour(self):
        if self.factor_to_change == 'hour':
            self.hour += 1
            if self.hour >= 24:
                self.hour -= 24
                self.factor_to_change = 'day'

    def __synchronize_day(self):
        if self.factor_to_change == 'day':
            self.day += 1
            if self.day >= 31:
                self.day -= 31
                self.factor_to_change = 'month'

    def __synchronize_month(self):
        if self.factor_to_change == 'month':
            self.month += 1
            if self.month >= 12:
                self.month -= 12
                self.factor_to_change = 'year'

    def __synchronize_year(self):
        if self.factor_to_change == 'year':
            self.year += 1

    @staticmethod
    def __get_current_datetime_splitted() -> [str]:
        return map(int, datetime.now().strftime('%d %m %Y %H %M').split())
