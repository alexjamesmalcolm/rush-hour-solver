from unittest import TestCase

from rush_hour import RushHourGame, RushHourCar, RushHourExit, Location


class TestRushHourGame(TestCase):
    def test_get_player_goal_as_4_1(self):
        player = RushHourCar(id=0, col=1, row=1, width=2, height=1)
        game = RushHourGame(
            board_size=6,
            cars=[
                player,
                RushHourCar(id=1, col=1, row=3, width=1, height=2),
            ],
            goal=RushHourExit(col=5, row=1, exit_direction="Right"),
        )

        self.assertEqual(game.get_player_goal(), Location(row=1, col=4))
