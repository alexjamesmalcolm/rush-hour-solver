from __future__ import annotations
from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from rush_hour import RushHourCar
    from solver import Movement


def simplify_results(
    results: List[Tuple[RushHourCar, Movement]],
) -> List[Tuple[RushHourCar, Movement]]:
    """This combines multiple 1 distance movements of the same car in the same direction into
    larger distance movements."""
    simplified_results: List[Tuple[RushHourCar, Movement]] = []
    for car, movement in results:
        if len(simplified_results) == 0:
            simplified_results.append((car, movement))
        else:
            last_car, last_movement = simplified_results[-1]
            if last_car == car and last_movement.direction == movement.direction:
                last_movement.distance += movement.distance
            else:
                simplified_results.append((car, movement))
    return simplified_results
