from unittest import TestCase

from rush_hour import RushHourGame, RushHourCar, RushHourExit
from solver import solve_game, Movement


class TestSolver(TestCase):
    def test_one_step_solution(self):
        self.maxDiff = 700
        player = RushHourCar(id=0, col=1, row=1, width=2, height=1)
        game = RushHourGame(
            board_size=6,
            cars=[
                player,
                RushHourCar(id=1, col=1, row=3, width=1, height=2),
            ],
            goal=RushHourExit(col=5, row=1, exit_direction="Right"),
        )

        steps = solve_game(game, max_turns=5)

        self.assertEqual(steps, [(player, Movement(direction="Right", distance=3))])

    def test_two_step_solution(self):
        self.maxDiff = 1500
        player = RushHourCar(id=0, col=1, row=1, width=2, height=1)
        other_car = RushHourCar(id=1, col=3, row=1, width=1, height=2)
        game = RushHourGame(
            board_size=6,
            cars=[
                player,
                other_car,
            ],
            goal=RushHourExit(col=5, row=1, exit_direction="Right"),
        )

        steps = solve_game(game, max_turns=10)

        self.assertEqual(
            steps,
            [
                (other_car, Movement(direction="Down", distance=1)),
                (player, Movement(direction="Right", distance=3)),
            ],
        )

    def test_level_one(self):
        """You can view the initial board state in docs/level-1.png"""
        player = RushHourCar(id=0, col=0, row=2, width=2, height=1)
        light_blue_car = RushHourCar(id=1, col=2, row=1, width=1, height=1)
        light_purple_truck = RushHourCar(id=2, col=0, row=3, width=3, height=1)
        blue_car = RushHourCar(id=3, col=0, row=4, width=1, height=2)
        pink_car = RushHourCar(id=4, col=1, row=4, width=1, height=2)
        purple_car = RushHourCar(id=5, col=2, row=4, width=1, height=2)
        yellow_truck = RushHourCar(id=6, col=4, row=1, width=1, height=3)
        orange_car = RushHourCar(id=7, col=5, row=2, width=1, height=2)
        turquoise_car = RushHourCar(id=8, col=4, row=4, width=2, height=1)
        grey_car = RushHourCar(id=9, col=4, row=5, width=2, height=1)

        game = RushHourGame(
            board_size=6,
            cars=[
                player,
                light_blue_car,
                light_purple_truck,
                blue_car,
                pink_car,
                purple_car,
                yellow_truck,
                orange_car,
                turquoise_car,
                grey_car,
            ],
            goal=RushHourExit(col=5, row=2, exit_direction="Right"),
        )

        steps = solve_game(game, max_turns=50)
        from pprint import pprint

        pprint(steps)
