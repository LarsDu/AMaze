from typing import Optional, Dict, List, Any

import pygame
from pygame import Color

from enum import Enum


class TileState(Enum):
    FLOOR_STATE = 0
    WALL_STATE = 1
    SEARCH_STATE = 2
    PATH_STATE = 3

class MazeCell:
    TILE_WIDTH = 3
    TILE_HEIGHT = 3
    CELL_WIDTH = TILE_WIDTH * 3
    CELL_HEIGHT = TILE_HEIGHT * 3
    WALL_COLOR: Color = Color(0,0,4,255),
    FLOOR_COLOR: Color = Color(255,255,255,255)
    SEARCH_COLOR: Color = Color(23,255,23,255)
    PATH_COLOR: Color = Color(22, 22, 255, 255) 

    STATE_TO_COLOR: Dict[int, Color] = {
        TileState.FLOOR_STATE: FLOOR_COLOR,
        TileState.WALL_STATE: WALL_COLOR,
        TileState.SEARCH_STATE: SEARCH_COLOR,
        TileState.PATH_STATE: PATH_COLOR,
    }

    #@property
    #def is_visited(self):
    #    return self.tiles[1][1] != 1

    def __lt__(self, other):
        """For sorting purposes, all maze cells are equal in value"""
        return False

    def __init__(
        self,
        row: int,
        col: int,
        canvas: Any = None,
    ):
        """ A 3x3 set of tiles wherein the outer tiles represent walls
        """
        self.row: int = row
        self.col: int = col
        self.tiles: List[List[int]] = [
            [TileState.WALL_STATE for _ in range(3)] for _ in range(3)
        ]
        self.canvas = canvas

    def draw(self):
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[0])):
                current_color = MazeCell.STATE_TO_COLOR.get(self.tiles[i][j], MazeCell.FLOOR_COLOR)
                pygame.draw.rect(
                    self.canvas,
                    current_color,
                    pygame.Rect(
                            self.col * MazeCell.CELL_WIDTH + j * MazeCell.TILE_WIDTH,
                            self.row * MazeCell.CELL_HEIGHT + i * MazeCell.TILE_HEIGHT,
                            MazeCell.TILE_WIDTH,
                            MazeCell.TILE_HEIGHT
                        )
                    )

    def connect(self, adjacent_row: int, adjacent_col: int, floor_state: TileState = TileState.FLOOR_STATE):
        """Remove the wall for the top, bottom, left, or right
        based on the coordinates of an adjacent MazeCell
        """
        if((abs(self.col-adjacent_col) > 1) or (abs(self.row-adjacent_row) > 1)):
            print(f"Can only connect adjacent cells ({self.col},{self.row}), ({adjacent_col},{adjacent_row})")
            return

        # Clear center tile
        self.tiles[1][1] = floor_state
        
        # Clear wall separating adjacent cell from this one
        self.tiles[1+adjacent_row - self.row][1+adjacent_col - self.col] = floor_state
        self.draw()

    def connect_cell(self, adjacent_cell: 'MazeCell', floor_state: TileState = TileState.FLOOR_STATE) -> None:
        self.connect(adjacent_cell.row, adjacent_cell.col, floor_state)
        adjacent_cell.connect(self.row, self.col, floor_state)
