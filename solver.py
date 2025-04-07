from typing import List, Tuple, Dict
from dataclasses import dataclass

from pulp import LpProblem, LpVariable, LpBinary, lpSum, LpMinimize

from rush_hour import RushHourGame, RushHourCar, Direction, Location


@dataclass
class Movement:
    distance: int
    direction: Direction


def solve_game(
    game: RushHourGame, max_turns: int = 100
) -> List[Tuple[RushHourCar, Movement]]:
    max_turns += 1
    p = LpProblem("Solve_Rush_Hour_Game", sense=LpMinimize)

    cars: Dict[RushHourCar, List[Dict[Location, LpVariable]]] = {
        car: [
            LpVariable.dicts(f"car_{car.id}_turn_{i}", game.grid, cat=LpBinary)
            for i in range(max_turns)
        ]
        for car in game.cars
    }

    # Constraint: Each car can only be in one location per turn
    for car in cars:
        for turn in range(max_turns):
            p += (
                lpSum(cars[car][turn].values()) == 1,
                f"car_{car.id}_on_turn_{turn}_must_be_in_one_location",
            )

    for car in cars:
        if car.direction == "HORIZONTAL":
            # Constraint: no horizontal car can exist on a row other than their original
            for turn in range(max_turns):
                p += (
                    lpSum(
                        variable
                        for location, variable in cars[car][turn].items()
                        if location.row == car.row
                    )
                    == 1,
                    f"car_{car.id}_on_turn_{turn}_must_be_on_row_{car.row}",
                )
        else:
            # Constraint: no vertical car can exist on a column other than their original
            for turn in range(max_turns):
                p += (
                    lpSum(
                        variable
                        for location, variable in cars[car][turn].items()
                        if location.col == car.col
                    )
                    == 1,
                    f"car_{car.id}_on_turn_{turn}_must_be_on_col_{car.col}",
                )

    # Constraint: no 2 cars can occupy the same cells on the same turn

    # Constraint: cars must be on the same side of cars in their line before and after a turn.
    # Meaning, a car can be on the left side of another car and must be prevented from teleporting
    # to the right side of the car.

    # Assign scores for each turn
    # p += lpSum(i *  for i in range(max_turns))

    print(p)
    return [(game.cars[0], Movement(direction="Right", distance=3))]
