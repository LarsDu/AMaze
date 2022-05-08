from enum import Enum
from itertools import chain

import pygame
from pygame import Color
from mazes.mazemap import MazeMap
from mazes.mazecell import MazeCell
from mazes.mazegen import MAZE
from mazes.mazesolver import SOLVERS
import click

@click.command()
@click.option(
    "--maze",
    "-m",
    type=str,
    default="prims"
)
@click.option(
    "--solver",
    "-s",
    type=str,
    default="astar"
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
    default=42
)
@click.option(
    "--tick",
    type=int,
    default=3000
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

    canvas = pygame.display.set_mode(((400+num_cols)*MazeCell.TILE_WIDTH, (400+num_rows)*MazeCell.TILE_HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Mazes")
    canvas.fill(Color(255,255,255,255))

    exit = False
    maze_map = MazeMap(num_rows, num_cols, canvas)
    maze_map.draw()
    maze_gen = MAZE[maze](maze_map, seed)
    maze_solver = SOLVERS[solver](maze_map, maze_map.cells[0][0], maze_map.cells[-1][-1])
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



