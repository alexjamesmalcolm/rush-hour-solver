from typing import List
from dataclasses import dataclass


@dataclass
class Location:
    col: int
    row: int


@dataclass
class RushHourCar(Location):
    is_player: bool
    width: int
    height: int

    @property
    def direction(self):
        if self.width > self.height:
            return "HORIZONTAL"
        return "VERTICAL"


@dataclass
class RushHourGame:
    board_size: int
    cars: List[RushHourCar]
    goal: Location
