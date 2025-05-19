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

    def test_get_player_goal_as_3_1(self):
        player = RushHourCar(id=0, col=1, row=1, width=3, height=1)
        game = RushHourGame(
            board_size=6,
            cars=[
                player,
                RushHourCar(id=1, col=1, row=3, width=1, height=2),
            ],
            goal=RushHourExit(col=5, row=1, exit_direction="Right"),
        )

        self.assertEqual(game.get_player_goal(), Location(row=1, col=3))

    def test_get_player_goal_as_3_2(self):
        player = RushHourCar(id=0, col=1, row=2, width=3, height=1)
        game = RushHourGame(
            board_size=6,
            cars=[
                player,
                RushHourCar(id=1, col=1, row=3, width=1, height=2),
            ],
            goal=RushHourExit(col=5, row=1, exit_direction="Right"),
        )

        self.assertEqual(game.get_player_goal(), Location(col=3, row=2))

    def test_get_player_goal_as_0_0(self):
        player = RushHourCar(id=0, col=0, row=2, width=1, height=2)
        game = RushHourGame(
            board_size=6,
            cars=[
                player,
                RushHourCar(id=1, col=1, row=3, width=1, height=2),
            ],
            goal=RushHourExit(col=0, row=0, exit_direction="Up"),
        )

        self.assertEqual(game.get_player_goal(), Location(col=0, row=0))

    def test_get_player_goal_as_1_0(self):
        player = RushHourCar(id=0, col=1, row=2, width=1, height=2)
        game = RushHourGame(
            board_size=6,
            cars=[
                player,
                RushHourCar(id=1, col=1, row=3, width=1, height=2),
            ],
            goal=RushHourExit(col=0, row=0, exit_direction="Up"),
        )

        self.assertEqual(game.get_player_goal(), Location(col=1, row=0))

    def test_get_player_goal_as_0_1(self):
        player = RushHourCar(id=0, col=4, row=1, width=2, height=1)
        game = RushHourGame(
            board_size=6,
            cars=[
                player,
                RushHourCar(id=1, col=1, row=3, width=1, height=2),
            ],
            goal=RushHourExit(col=0, row=0, exit_direction="Left"),
        )

        self.assertEqual(game.get_player_goal(), Location(col=0, row=1))

    def test_get_player_goal_as_1_4(self):
        player = RushHourCar(id=0, col=1, row=1, width=1, height=2)
        game = RushHourGame(
            board_size=6,
            cars=[
                player,
                RushHourCar(id=1, col=1, row=3, width=1, height=2),
            ],
            goal=RushHourExit(col=0, row=0, exit_direction="Down"),
        )

        self.assertEqual(game.get_player_goal(), Location(col=1, row=4))

    def test_get_player_goal_as_2_3(self):
        player = RushHourCar(id=0, col=2, row=1, width=1, height=3)
        game = RushHourGame(
            board_size=6,
            cars=[
                player,
                RushHourCar(id=1, col=1, row=3, width=1, height=2),
            ],
            goal=RushHourExit(col=0, row=0, exit_direction="Down"),
        )

        self.assertEqual(game.get_player_goal(), Location(col=2, row=3))

    def test_end_is_right_of_start(self):
        start = Location(col=1, row=1)
        end = Location(col=2, row=1)

        result = start.compare_direction(end)

        self.assertEqual(result, "Right")

    def test_end_is_down_from_start(self):
        start = Location(col=1, row=1)
        end = Location(col=1, row=2)

        result = start.compare_direction(end)

        self.assertEqual(result, "Down")

    def test_end_is_up_from_start(self):
        start = Location(col=1, row=1)
        end = Location(col=1, row=0)

        result = start.compare_direction(end)

        self.assertEqual(result, "Up")

    def test_end_is_left_of_start(self):
        start = Location(col=1, row=1)
        end = Location(col=0, row=1)

        result = start.compare_direction(end)

        self.assertEqual(result, "Left")
