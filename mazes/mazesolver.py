""" Pathfinding algorithms for traversing a maze
"""
from enum import Enum
import heapq
from collections import deque

from typing import Tuple, Dict, Set, List, Any

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
            # First path, not shortest
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
    min_heap: List[Any] = [(float('inf'), start)]

    #visited: List[List[bool]] = [
    #    [False for _ in range(maze_map.num_columns)] for _ in range(maze_map.num_rows)
    #]

    g_scores: List[List[float]] = [
        [float('inf') for _ in range(maze_map.num_columns)] for _ in range(maze_map.num_rows)
    ]
    g_scores[start.row][start.col] = 0

   
    parents: Dict[MazeCell, MazeCell] = {
        start: None
    }

    is_found: bool = False

    while min_heap or not is_found:
        # Extract unvisited item with lowest f-score and visit "current"
        try:
            fscore, current = heapq.heappop(min_heap)
        except IndexError:
            print("IndexError when extracting from min_heap")
            break
        #visited[current.row][current.col] = True

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
                nc < maze_map.num_columns
                #not visited[nr][nc]
            ):
                query: MazeCell = maze_map.cells[nr][nc]
                if(maze_map.query_connected(current, query)):
                    tentative_g = 1+g_scores[current.row][current.col]
                    if(tentative_g < g_scores[nr][nc]):
                        # Replace g-score here with the lower cost path
                        g_scores[nr][nc] = tentative_g
                        # Calculate manhaddan heuristic for this current neighbor
                        h_score = abs(end.row - nr) + abs(end.col - nc)
                        # Compute f_score
                        f_score = tentative_g + h_score
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


def double_bfs(maze_map: MazeMap, start: MazeCell, end: MazeCell) -> None:
    """Find a path through a maze with a layer-wise
    breadth-first from both start and end
    """
    dq = deque([(start, TileState.START_SEARCH_STATE), (end, TileState.END_SEARCH_STATE)])
    # Use to 1s to mark searches from start and 2s to mark searches from end
    visited: List[List[int]] = [ [TileState.FLOOR_STATE for _ in range(maze_map.num_columns)] for _ in range(maze_map.num_rows)]
    parents: Dict[MazeCell, MazeCell] = dict() #TODO Replace with linked list
    is_found = False
    terminus_a = None
    terminus_b = None
    while dq and not is_found:
        # Visit the entirety of the current layer
        for _ in range(len(dq)):
            # Visit current cell
            current_cell, current_origin = dq.popleft()
            #visited[current_cell.row][current_cell.col] = 1
            yield False
            # Visit conneected neighbors in bounds
            for dr, dc in DIRECTIONS:
                nr, nc = current_cell.row + dr, current_cell.col + dc
                if(
                    nr >= 0 and
                    nr < maze_map.num_rows and
                    nc >= 0 and
                    nc < maze_map.num_columns
                ):
                    neighbor_cell = maze_map.cells[nr][nc]
                    if(visited[nr][nc] == TileState.FLOOR_STATE):
                        # If un-visited, add connected neighbor to queue
                        if (maze_map.query_connected(current_cell, neighbor_cell, current_origin)):
                            parents[neighbor_cell] = current_cell
                            visited[nr][nc] = current_origin
                            dq.append((neighbor_cell, current_origin))
                    elif(visited[nr][nc] != current_origin):
                        # Final path possibly located                    
                        if (maze_map.query_connected(current_cell, neighbor_cell, current_origin)):
                            terminus_a = neighbor_cell
                            terminus_b = current_cell
                            #parents[neighbor_cell] = current_cell
                            is_found = True
                            # Reverse the parents path for one of the directions.
                            #break;
         
    for terminus in (terminus_a, terminus_b):
        cur = terminus
        prev = terminus
        while cur and cur != start:
            cur = parents[cur]
            cur.connect_cell(prev, floor_state=TileState.PATH_STATE)
            yield True
            prev = cur
        yield True


SOLVER = {
    "dfs": dfs,
    "dijkstra": dijkstra,
    "astar": astar,
    "double_bfs": double_bfs
}
