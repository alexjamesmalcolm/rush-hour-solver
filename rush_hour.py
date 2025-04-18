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

    def is_on_path(self, location: Location) -> bool:
        if self.direction == "HORIZONTAL":
            return location.row == self.row
        return location.col == self.col


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
        return Location(col=player.col, row=self.board_size - player.height)


def get_grid(size: int) -> List[Location]:
    grid = []
    for x in range(size):
        for y in range(size):
            grid.append(Location(x, y))
    return grid
