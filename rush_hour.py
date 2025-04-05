from typing import List, Literal
from dataclasses import dataclass


Direction = Literal["Top", "Bottom", "Left", "Right"]


@dataclass
class Location:
    col: int
    row: int


@dataclass
class RushHourExit(Location):
    exit_direction: Direction


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
    goal: RushHourExit
