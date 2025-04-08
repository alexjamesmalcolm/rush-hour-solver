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

    @property
    def player(self) -> RushHourCar:
        for car in self.cars:
            if car.id == 0:
                return car
        raise Exception("Could not find player")

    def get_player_goal(self) -> Location:
        player = self.player
        if self.goal.exit_direction == "Right":
            return Location(col=self.board_size - player.width, row=player.row)
        if self.goal.exit_direction == "Up":
            return Location(col=self.player.col, row=0)
        if self.goal.exit_direction == "Left":
            return Location(col=0, row=self.player.row)
        return Location(col=1, row=4)


def get_grid(size: int) -> List[Location]:
    grid = []
    for x in range(size):
        for y in range(size):
            grid.append(Location(x, y))
    return grid
