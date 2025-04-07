import random
import tkinter as tk

from rush_hour import RushHourGame, RushHourCar


def random_color():
    return "#{:06x}".format(random.randint(0, 0x88FFFF))


class RushHourGameVisualization:
    def __init__(self, game: RushHourGame, size: int = 300):
        self.game = game
        self.size = size

    def draw_grid(self, canvas: tk.Canvas) -> None:
        cell_size = self.size // self.game.board_size
        for i in range(self.game.board_size + 1):
            # Vertical lines
            canvas.create_line(
                i * cell_size, 0, i * cell_size, self.size, fill="grey", width=2
            )
            # Horizontal lines
            canvas.create_line(
                0, i * cell_size, self.size, i * cell_size, fill="gray", width=2
            )

    def draw_car(self, canvas: tk.Canvas, car: RushHourCar) -> None:
        cell_size = self.size // self.game.board_size
        canvas.create_rectangle(
            car.col * cell_size,
            car.row * cell_size,
            car.col * cell_size + car.width * cell_size,
            car.row * cell_size + car.height * cell_size,
            fill="red" if car.id == 0 else random_color(),
        )

    def draw_exit(self, canvas: tk.Canvas) -> None:
        cell_size = self.size // self.game.board_size
        col = self.game.goal.col
        row = self.game.goal.row
        x = col * cell_size
        y = row * cell_size

        if self.game.goal.exit_direction == "Top":
            canvas.create_line(x, y, x + cell_size, y, fill="red", width=4)
        elif self.game.goal.exit_direction == "Bottom":
            canvas.create_line(
                x, y + cell_size, x + cell_size, y + cell_size, fill="red", width=4
            )
        elif self.game.goal.exit_direction == "Left":
            canvas.create_line(x, y, x, y + cell_size, fill="red", width=4)
        elif self.game.goal.exit_direction == "Right":
            canvas.create_line(
                x + cell_size, y, x + cell_size, y + cell_size, fill="red", width=4
            )

    def visualize(self):
        root = tk.Tk()
        canvas = tk.Canvas(root, width=self.size, height=self.size)
        canvas.pack()
        self.draw_grid(canvas)
        for car in self.game.cars:
            self.draw_car(canvas, car)
        self.draw_exit(canvas)
        root.mainloop()
