""" Maze generation algorithms

DFS uses a stack, BFS uses a deque, and Prim's uses a set
"""

from enum import Enum

from typing import Dict, Set, List, Tuple, Any
import random
from collections import deque
from mazes.mazemap import MazeMap
from mazes.mazecell import MazeCell, TileState
from mazes.constants import DIRECTIONS


def generate_dfs_maze(maze_map: MazeMap, seed: int = 42) -> bool:
    """ Generate a maze using randomized depth-first search
    """
    random.seed(seed)
    directions = list(DIRECTIONS)
    stack: List[Tuple[int]] = [(0,0)]
    visited = [ [False for _ in range(maze_map.num_columns)] for _ in range(maze_map.num_rows)]
    parent: Dict[Tuple[int], Tuple[int]] = {(0,0):(0,0)}
    while stack:
        cr, cc = stack.pop()
        # Visit the current cell
        current_cell: MazeCell = maze_map.cells[cr][cc]
        pr, pc = parent[(cr,cc)]
        parent_cell: MazeCell = maze_map.cells[pr][pc]
        current_cell.connect(pr, pc)
        parent_cell.connect(cr, cc)
        visited[cr][cc] = True
        yield False
        # Shuffle
        random.shuffle(directions)

        # Append valid neighbors to queue
        for dr, dc in directions:                        
            nr = cr+dr
            nc = cc+dc
            # Add to stack if not previously visited
            if(nc < maze_map.num_columns and
                nc >= 0 and 
                nr < maze_map.num_rows and
                nr >= 0 and 
                not visited[nr][nc]
            ):
                stack.append((nr, nc))
                parent[(nr,nc)] = (cr,cc)
        
    yield True


def generate_bfs_maze(maze_map: MazeMap, seed: int = 42) -> bool:
    """ Generate a maze using randomized breadth-first search

    This winds up being quite slow as most expansion directions are not valid
    after a while
    """
    random.seed(seed)
    directions = list(DIRECTIONS)
    dq: deque[Tuple[int]] = deque([(0,0)])
    visited = [ [False for _ in range(maze_map.num_columns)] for _ in range(maze_map.num_rows)]
    parent: Dict[Tuple[int], Tuple[int]] = {(0,0):(0,0)}
    while dq:
        cr, cc = dq.popleft()
        # Visit the current cell
        current_cell: MazeCell = maze_map.cells[cr][cc]
        pr, pc = parent[(cr,cc)]
        parent_cell: MazeCell = maze_map.cells[pr][pc]
        current_cell.connect(pr, pc)
        parent_cell.connect(cr, cc)
        visited[cr][cc] = True
        yield False
        # Shuffle
        random.shuffle(directions)

        # Append valid neighbors to queue
        for dr, dc in directions:
            nc = cc+dc
            nr = cr+dr
            # Add to stack if not previously visited
            if(nc < maze_map.num_columns and
                nc >= 0 and 
                nr < maze_map.num_rows and
                nr >= 0 and not visited[nr][nc]):
                dq.append((nr, nc))
                parent[(nr,nc)] = (cr,cc)
        
    yield True

def generate_prims_maze(maze_map: MazeMap, seed:int = 42) -> bool:
    """ Generate a maze using randomized Prim's algorithm

    https://hurna.io/academy/algorithms/maze_generator/prim_s.html
    """
    random.seed(seed)
    directions = list(DIRECTIONS)
    cell_set: Set[Tuple[int]] = {(0,0)}
    visited = [ [False for _ in range(maze_map.num_columns)] for _ in range(maze_map.num_rows)]
    parent: Dict[Tuple[int], Tuple[int]] = {(0,0):(0,0)}
    while len(cell_set) > 0:
        random_cell = cell_set.pop()
        cr, cc = random_cell
        # Visit the current cell
        current_cell: MazeCell = maze_map.cells[cr][cc]
        pr, pc = parent[(cr,cc)]
        parent_cell: MazeCell = maze_map.cells[pr][pc]
        current_cell.connect(pr, pc)
        parent_cell.connect(cr, cc)
        visited[cr][cc] = True
        yield False
        # Shuffle

        # Prim's does not NEED a directional shuffle
        # however shuffling here allows us to use a random seed
        random.shuffle(directions)

        # Append valid neighbors to queue
        for dr, dc in directions:
            nc = cc+dc
            nr = cr+dr
            # Add to stack if not previously visited
            if(nc < maze_map.num_columns and
                nc >= 0 and 
                nr < maze_map.num_rows and
                nr >= 0 and not visited[nr][nc]):
                cell_set.add((nr, nc))
                parent[(nr,nc)] = (cr,cc)
        
    yield True

MAZE = {
    "dfs": generate_dfs_maze,
    "bfs": generate_bfs_maze,
    "prims": generate_prims_maze,
}