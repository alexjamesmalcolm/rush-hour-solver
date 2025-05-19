from unittest import TestCase
from solver_utils import simplify_results
from rush_hour import RushHourCar
from solver import Movement


class TestSimplifyResults(TestCase):
    def test_simplify_two_rights_into_a_single_movement(self):
        car = RushHourCar(col=1, row=1, id=0, width=2, height=1)
        results = simplify_results(
            [
                (car, Movement(direction="Right", distance=1)),
                (car, Movement(direction="Right", distance=1)),
            ]
        )

        self.assertEqual(results, [(car, Movement(direction="Right", distance=2))])
