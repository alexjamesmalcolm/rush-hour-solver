from typing import List, Tuple, Dict
from dataclasses import dataclass

from pulp import (
    LpProblem,
    LpVariable,
    LpBinary,
    lpSum,
    LpMaximize,
    PULP_CBC_CMD,
    permutation,
)

from rush_hour import RushHourGame, RushHourCar, Direction, Location
from lp_utils import add_constraints, lp_and
from solver_utils import simplify_results


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

    car_turn_movement: Dict[
        RushHourCar, List[Dict[Tuple[Location, Location], LpVariable]]
    ] = {}
    for car in game.cars:
        locations_on_path = [
            location for location in game.grid if car.is_on_path(location)
        ]
        movements = [
            (start, end)
            for start, end in permutation(locations_on_path, 2)
            # if start.distance(end) == 1
        ]
        car_turn_movement[car] = [
            LpVariable.dicts(
                f"car_{car.id}_turn_{turn}_movement", movements, cat=LpBinary
            )
            for turn in range(0, max_turns)
        ]

    # Constraint: Defining car_turn_movement by the values of car_turn_position
    for car in car_turn_position:
        for turn in range(1, max_turns):
            movements = car_turn_movement[car][turn]
            for (start, end), movement_variable in movements.items():
                previous_position = car_turn_position[car][turn - 1][start]
                current_position = car_turn_position[car][turn][end]
                name = (
                    "defining_"
                    + str(movement_variable)
                    + "_as_"
                    + str(current_position)
                    + "_and_"
                    + str(previous_position)
                )
                p = add_constraints(
                    p,
                    lp_and(
                        a=current_position,
                        b=previous_position,
                        answer=movement_variable,
                        name=name,
                    ),
                )

    # Constraint: Preventing teleportation movements in car_turn_movement
    for car, turn_movement in car_turn_movement.items():
        for turn in range(1, max_turns):
            movements = turn_movement[turn]
            for (start, end), movement_variable in movements.items():
                if start.distance(end) > 1:
                    p += movement_variable == 0

    # Constraint: One car must move per turn
    for turn in range(1, max_turns):
        p += (
            lpSum(
                move
                for car in game.cars
                for move in car_turn_movement[car][turn].values()
            )
            == 1,
            f"one_car_must_move_on_turn_{turn}",
        )

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
    for car_a, car_b in permutation(game.cars, 2):
        for car_a_position in game.grid:
            if not car_a.is_on_path(car_a_position):
                continue
            car_a_occupied_locations = car_a.get_occupied_locations(car_a_position)
            for car_b_position in game.grid:
                if not car_b.is_on_path(car_b_position):
                    continue
                car_b_occupied_locations = car_b.get_occupied_locations(car_b_position)
                do_cars_collide = any(
                    car_a_occupied_location == car_b_occupied_location
                    for car_a_occupied_location in car_a_occupied_locations
                    for car_b_occupied_location in car_b_occupied_locations
                )
                if do_cars_collide:
                    for turn in range(max_turns):
                        p += (
                            car_turn_position[car_a][turn][car_a_position]
                            + car_turn_position[car_b][turn][car_b_position]
                            <= 1
                        )

    # Constraint: cars must be on the same side of cars in their line before and after a turn.
    # Meaning, a car can be on the left side of another car and must be prevented from teleporting
    # to the right side of the car.

    # Constraint: Need to define speed of each car as the change in position per turn

    # Constraint: Need to figure out a way to have 1 car move per turn by constraining speed

    # Assign scores for each turn
    def is_player_at_goal(turn: int) -> LpVariable:
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

    p.solve(PULP_CBC_CMD(msg=False))

    for turns in car_turn_movement.values():
        for turn in range(max_turns):
            for variable in turns[turn].values():
                if variable.varValue == 1:
                    print(f"{variable} == 1")
    if p.objective:
        print(p.objective.value())
    else:
        raise Exception("Why does the problem not have an objective?")

    for turn in range(max_turns):
        value_of_turn = is_player_at_goal(turn)
        print(f"Turn {turn} score: {value_of_turn} == {value_of_turn.value()}")

    print(f"The goal is {game.get_player_goal()}")
    results: List[Tuple[RushHourCar, Movement]] = []
    for turn in range(max_turns):
        for car, turn_movement in car_turn_movement.items():
            for (start, end), variable in turn_movement[turn].items():
                if variable.varValue == 1:
                    print(f"Car {car.id} on turn {turn} moved from {start} to {end}")
                    results.append(
                        (
                            car,
                            Movement(
                                distance=int(start.distance(end)),
                                direction=start.compare_direction(end),
                            ),
                        )
                    )
            if is_player_at_goal(turn).varValue == 1:
                return simplify_results(results)
    raise Exception("No solution found")
