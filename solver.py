from typing import List, Tuple, Dict
from dataclasses import dataclass

from pulp import (
    LpProblem,
    LpVariable,
    LpBinary,
    lpSum,
    LpMaximize,
    LpAffineExpression,
    PULP_CBC_CMD,
)

from rush_hour import RushHourGame, RushHourCar, Direction, Location


@dataclass
class Movement:
    distance: int
    direction: Direction


def solve_game(
    game: RushHourGame, max_turns: int = 100
) -> List[Tuple[RushHourCar, Movement]]:
    max_turns += 1
    p = LpProblem("Solve_Rush_Hour_Game", sense=LpMaximize)

    car_turn_position: Dict[RushHourCar, List[Dict[Location, LpVariable]]] = {
        car: [
            LpVariable.dicts(f"car_{car.id}_turn_{i}_position", game.grid, cat=LpBinary)
            for i in range(max_turns)
        ]
        for car in game.cars
    }

    turn_car_active: List[Dict[RushHourCar, LpVariable]] = [
        LpVariable.dicts(f"turn_{i}_car_active", game.cars, cat=LpBinary)
        for i in range(max_turns)
    ]
    for car in car_turn_position:
        for turn in range(max_turns):
            car_moved_positively_on_this_turn = LpVariable(
                f"car_{car.id}_on_turn_{turn}_moved_forward", cat=LpBinary
            )
            car_moved_negatively_on_this_turn = LpVariable(
                f"car_{car.id}_on_turn_{turn}_moved_backward", cat=LpBinary
            )
            p += car_moved_positively_on_this_turn >= lpSum
            # Taking a single row as an example, I think I'm supposed to do something like assign each cell in the row an increasing value. Then take the lpSum of a row on turn i and take the difference between that lpSum and the lpSum of the same row on turn i + 1. Then I will make car_moved_positively_on_this_turn >= that difference. I'm not sure how it would work for the car moving negatively but it can't be that different.

    # Constraint: Need to define speed of each car as the change in position per turn

    # Constraint: The first turn is set by initial parameters
    for car in car_turn_position:
        for location, variable in car_turn_position[car][0].items():
            if location.row == car.row and location.col == car.col:
                p += variable == 1, f"car_{car.id}_starts_at_{location}"

    # Constraint: Each car can only be in one location per turn
    for car in car_turn_position:
        for turn in range(max_turns):
            p += (
                lpSum(car_turn_position[car][turn].values()) == 1,
                f"car_{car.id}_on_turn_{turn}_must_be_in_one_location",
            )

    for car in car_turn_position:
        if car.direction == "HORIZONTAL":
            # Constraint: no horizontal car can exist on a row other than their original
            for turn in range(max_turns):
                p += (
                    lpSum(
                        variable
                        for location, variable in car_turn_position[car][turn].items()
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
                        for location, variable in car_turn_position[car][turn].items()
                        if location.col == car.col
                    )
                    == 1,
                    f"car_{car.id}_on_turn_{turn}_must_be_on_col_{car.col}",
                )

    # Constraint: no 2 cars can occupy the same cells on the same turn

    # Constraint: cars must be on the same side of cars in their line before and after a turn.
    # Meaning, a car can be on the left side of another car and must be prevented from teleporting
    # to the right side of the car.

    # Constraint: Need to define speed of each car as the change in position per turn

    # Constraint: Need to figure out a way to have 1 car move per turn by constraining speed

    # Assign scores for each turn
    def is_player_at_goal(turn: int) -> LpAffineExpression:
        player = None
        for car in car_turn_position:
            if car.id == 0:
                player = car
        if not player:
            raise Exception("Player not found")
        current_turn = car_turn_position[player][turn]
        goal_location = game.get_player_goal()
        for location, variable in current_turn.items():
            if location == goal_location:
                return variable
        raise Exception("Could not find goal_location in current_turn")

    p += lpSum(is_player_at_goal(i) for i in range(max_turns))

    p.solve(PULP_CBC_CMD(msg=0))
    print(p)

    for variable in p.variables():
        if variable.varValue == 1:
            print(variable)
    return [(game.cars[0], Movement(direction="Right", distance=3))]
