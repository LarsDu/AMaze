""" Pathfinding algorithms for traversing a maze
"""
from enum import Enum
import heapq

from typing import Tuple, Dict, Set, List

from mazes.mazemap import MazeMap
from mazes.mazecell import MazeCell, TileState
from mazes.constants import DIRECTIONS 



def dfs(
    maze_map: MazeMap,
    start: MazeCell,
    end: MazeCell
) -> bool:
    stack = [start]
    visited: List[List[bool]] = [[False for _ in range(maze_map.num_columns)] for _ in range(maze_map.num_rows)]
    visited[start.row][start.col] = True
    parents: Dict[MazeCell, MazeCell] = {
        start: None
    }
    is_found: bool = False

    while stack and not is_found:
        current: MazeCell = stack.pop()
        ## Visit current
        if(current == end):
            # Found solution
            stack.clear()
            is_found = True
            yield True
        else:
            yield False

        for dr, dc in DIRECTIONS:
            nr = current.row + dr
            nc = current.col + dc
            if(
                nc >= 0 and
                nc < maze_map.num_columns and
                nr >= 0 and
                nr < maze_map.num_rows and
                not visited[nr][nc]
            ):
                query = maze_map.cells[nr][nc]
                is_connected: bool = maze_map.query_connected(current, query)
                if is_connected:
                    visited[nr][nc] = True
                    parents[query] = current
                    stack.append(query)

    # Backtrace the found path
    cur: MazeCell = end
    prev: MazeCell = end

    while cur != start:
        cur = parents[cur]
        cur.connect_cell(prev, floor_state=TileState.PATH_STATE)
        yield True
        prev = cur


def dijkstra(
        maze_map: MazeMap,
        start: MazeCell,
        end: MazeCell,
    ) -> None:
    """ Generate a path through two points in maze using dijkstra's algorithm
    """
    # Insert a tuple of (distance, MazeCell)
    min_heap: List[int] = [(0,start)]

    visited: List[List[bool]] = [
        [False for _ in range(maze_map.num_columns)] for _ in range(maze_map.num_rows)
    ]
   
    parents: Dict[MazeCell, MazeCell] = {
        start: None
    }
    is_found: bool = False

    while min_heap or not is_found:
        # Extract item with lowest distance and visit "current"
        try:
            cdist, current = heapq.heappop(min_heap)
        except IndexError:
            print("IndexError when extracting from min_heap")
            break
        visited[current.row][current.col] = True

        if(current == end):
            is_found = True
            yield True
            break
        else:
            yield False

        # For each neighbor determine if connected, and push to min_heap if so
        for drow, dcol in DIRECTIONS:
            nr, nc = current.row + drow, current.col + dcol
            if(
                nr >= 0 and
                nc >= 0 and
                nr < maze_map.num_rows and
                nc < maze_map.num_columns and
                not visited[nr][nc]
            ):
                query: MazeCell = maze_map.cells[nr][nc]
                is_connected: bool = maze_map.query_connected(current, query)
                if(is_connected):
                    heapq.heappush(min_heap, (cdist+1, query))
                    parents[query] = current
        

    # Backtrace the found path
    cur: MazeCell = end
    prev: MazeCell = end

    while cur != start:
        cur = parents[cur]
        cur.connect_cell(prev, floor_state=TileState.PATH_STATE)
        yield True
        prev = cur




def astar(maze_map: MazeMap, start: MazeCell, end: MazeCell) -> None:
    """ Generate a path between two points in a maze using A*
    """
      # Insert a tuple of (distance, MazeCell)
    min_heap: List[int] = [(float('inf'),start)]

    visited: List[List[bool]] = [
        [False for _ in range(maze_map.num_columns)] for _ in range(maze_map.num_rows)
    ]
   
    parents: Dict[MazeCell, MazeCell] = {
        start: None
    }

    is_found: bool = False

    while min_heap or not is_found:
        # Extract item with lowest distance and visit "current"
        try:
            cdist, current = heapq.heappop(min_heap)
        except IndexError:
            print("IndexError when extracting from min_heap")
            break
        visited[current.row][current.col] = True

        if(current == end):
            is_found = True
            yield True
            break
        else:
            yield False

        # For each neighbor determine if connected, and push to min_heap if so
        for drow, dcol in DIRECTIONS:
            nr, nc = current.row + drow, current.col + dcol
            if(
                nr >= 0 and
                nc >= 0 and
                nr < maze_map.num_rows and
                nc < maze_map.num_columns and
                not visited[nr][nc]
            ):
                query: MazeCell = maze_map.cells[nr][nc]
                g_score = abs((end.row - nr)**2 + (end.col - nc)**2)
                h_score = abs((start.row - nr)**2 + (end.col - nc)**2)
                f_score = g_score + h_score
                is_connected: bool = maze_map.query_connected(current, query)
                if(is_connected):
                    heapq.heappush(min_heap, (f_score, query))
                    parents[query] = current
        

    # Backtrace the found path
    cur: MazeCell = end
    prev: MazeCell = end

    while cur != start:
        cur = parents[cur]
        cur.connect_cell(prev, floor_state=TileState.PATH_STATE)
        yield True
        prev = cur


SOLVER = {
    "dfs": dfs,
    "dijkstra": dijkstra,
    "astar": astar
}
