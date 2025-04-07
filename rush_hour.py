from typing import List, Literal
from dataclasses import dataclass


Direction = Literal["Up", "Down", "Left", "Right"]


@dataclass
class Location:
    col: int
    row: int

    def __hash__(self):
        return (self.col, self.row).__hash__()


@dataclass
class RushHourExit(Location):
    exit_direction: Direction


@dataclass
class RushHourCar(Location):
    id: int
    width: int
    height: int

    def __hash__(self):
        return self.id

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

    @property
    def grid(self):
        return get_grid(self.board_size)

    def get_player_goal(self) -> Location:
        return Location(col=4, row=1)


def get_grid(size: int) -> List[Location]:
    grid = []
    for x in range(size):
        for y in range(size):
            grid.append(Location(x, y))
    return grid
