from unittest import TestCase

from rush_hour import RushHourGame, RushHourCar, RushHourExit
from solver import solve_game, Movement


class TestSolver(TestCase):
    def test_one_step_solution(self):
        player = RushHourCar(col=1, row=1, is_player=True, width=2, height=1)
        game = RushHourGame(
            board_size=6,
            cars=[
                player,
                RushHourCar(col=1, row=3, is_player=False, width=1, height=2),
            ],
            goal=RushHourExit(col=5, row=1, exit_direction="Right"),
        )

        steps = solve_game(game)

        self.assertEqual(steps, [(player, Movement(direction="Right", distance=3))])

    def test_two_step_solution(self):
        player = RushHourCar(col=1, row=1, is_player=True, width=2, height=1)
        other_car = RushHourCar(col=3, row=1, is_player=False, width=1, height=2)
        game = RushHourGame(
            board_size=6,
            cars=[
                player,
                other_car,
            ],
            goal=RushHourExit(col=5, row=1, exit_direction="Right"),
        )

        steps = solve_game(game)

        self.assertEqual(
            steps,
            [
                (other_car, Movement(direction="Down", distance=1)),
                (player, Movement(direction="Right", distance=3)),
            ],
        )
