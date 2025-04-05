from unittest import TestCase

from rush_hour import RushHourGame, RushHourCar, RushHourExit
from solver import solve_game


class TestSolver(TestCase):
    def test_one_step_solution(self):
        game = RushHourGame(
            board_size=6,
            cars=[
                RushHourCar(col=1, row=1, is_player=True, width=2, height=1),
                RushHourCar(col=1, row=3, is_player=False, width=1, height=2),
            ],
            goal=RushHourExit(col=5, row=1, exit_direction="Right"),
        )

        steps = solve_game(game)

        self.assertEqual(len(steps), 1)
