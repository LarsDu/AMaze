from enum import Enum
from itertools import chain

import pygame
from pygame import Color
from mazes.mazemap import MazeMap
from mazes.mazecell import MazeCell
from mazes.mazegen import MAZE
from mazes.mazesolver import SOLVER
import click

@click.command()
@click.option(
    "--maze",
    "-m",
    type=str,
    default="prims",
    help=f"Maze type from {list(MAZE.keys())}"
)
@click.option(
    "--solver",
    "-s",
    type=str,
    default="astar",
    help=f"Path solver from {list(SOLVER.keys())}"
)
@click.option(
    "--num_rows",
    "-r",
    type=int,
    default=100
)
@click.option(
    "--num_cols",
    "-c",
    type=int,
    default=100
)
@click.option(
    "--seed",
    type=int,
    default=42,
    help="Random seed for maze generation"
)
@click.option(
    "--tick",
    type=int,
    default=3000,
    help="Tick rate. Higher means faster maze generation"
)
def main(
    maze,
    solver,
    num_rows: int,
    num_cols: int,
    seed: int,
    tick: int
):
    pygame.init()

    scale = MazeCell.TILE_HEIGHT
    canvas = pygame.display.set_mode((scale*(num_cols+1)*MazeCell.TILE_WIDTH, scale*(num_rows+1)*MazeCell.TILE_HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Mazes")
    canvas.fill(Color(255,255,255,255))

    exit = False
    maze_map = MazeMap(num_rows, num_cols, canvas)
    maze_map.draw()
    maze_gen = MAZE[maze](maze_map, seed)
    maze_solver = SOLVER[solver](maze_map, maze_map.cells[0][0], maze_map.cells[-1][-1])
    chain_gen = chain(maze_gen, maze_solver)
    while not exit:
        try:
            next(chain_gen)
        except StopIteration:
            pass
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
        clock.tick(tick)
        pygame.display.update()
if __name__ == "__main__":
    main()



