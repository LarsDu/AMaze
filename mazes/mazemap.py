

from lib2to3.pgen2 import driver
from typing import Any, Dict, List, Optional

import pygame
from pygame import Color
from mazes.mazecell import MazeCell, TileState

class MazeMap:

    @property
    def num_columns(self):
        return len(self.cells[0])

    @property
    def num_rows(self):
        return len(self.cells)

    def __init__(self, num_rows: int, num_columns: int, canvas: Any) -> None:
        """ A 2D grid of MazeCells
        
        Args:
            num_rows: Number of cells across
            num_columns: Number of cells down
        
        """
        self.canvas = canvas
        self.cells: List[List[MazeCell]] = [
            [MazeCell(i,j, self.canvas) for j in range(num_columns)] for i in range(num_rows)
        ]


    def draw(self) -> None:
        """ Draw the MazeMap
        """
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                self.cells[i][j].draw()


    def query_connected(self, a: MazeCell, b: Optional[MazeCell], query_state: int = TileState.SEARCH_STATE) -> bool:
        """ Determine if cells a and b are connected
        
        Also changes the floor color to a search color
        """
        if(a == b or not b):
            a.tiles[1][1] = TileState.SEARCH_STATE
            return True
        dr = b.row - a.row
        dc = b.col - a.col
        # Recolor dividing walls
        war = 1 + dr
        wac = 1 + dc
        wbr = 1 - dr
        wbc = 1 - dc
        if( abs(dr) <= 1 and
            abs(dc) <= 1 and
            a.tiles[1][1] != TileState.WALL_STATE and
            b.tiles[1][1] != TileState.WALL_STATE and
            a.tiles[war][wac] != TileState.WALL_STATE and 
            b.tiles[wbr][wbc] != TileState.WALL_STATE
        ):
            a.tiles[1][1] = query_state
            b.tiles[1][1] = query_state
            # Set the connecting walls to have search state
            a.tiles[war][wac] = query_state
            b.tiles[wbr][wbc] = query_state
            a.draw()
            b.draw()
            return True

        a.draw()
        b.draw()
        return False

