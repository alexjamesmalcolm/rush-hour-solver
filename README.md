# Rush Hour Solver

Rush Hour is a game where the objective is to free a red car from the board. You can move any car on the board but only into an empty space that is available. There is a hole just big enough for the red car to escape through. No other cars are allowed to escape.

## Motivation

The reason for creating this solver is because it is a good intermediary step between different kinds of solvers that I want to make. The most recent solver that I worked on was for a game called Queens but I would eventually like to make optimizers for situations that involve time-steps of seconds or milliseconds rather than turns. This game does involve steps, only one car can be moved at a time, and a solution could be optimized with the objective of completing a game using the fewest number of steps.
