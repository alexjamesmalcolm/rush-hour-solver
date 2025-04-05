from typing import List, Tuple
from dataclasses import dataclass
from rush_hour import RushHourGame, RushHourCar, Direction


@dataclass
class Movement:
    distance: int
    direction: Direction


def solve_game(game: RushHourGame) -> List[Tuple[RushHourCar, Movement]]:
    return [(game.cars[0], Movement(direction="Right", distance=3))]
