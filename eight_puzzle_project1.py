"""
CS170 Project 1: 8-Puzzle Solver

Authors: Shreyas, Rishith, Rehan
"""

from typing import List, Tuple
from copy import deepcopy

class PuzzleState:
    """Represents the state of an 8-puzzle configuration."""
    
    def __init__(self, grid: List[List[int]]):
        """
        Initialize puzzle state with a 3x3 grid.
        0 represents the blank tile.
        """
        self.grid = grid
        self.size = len(grid)
        self.blank_pos = self._find_blank()
    
    def _find_blank(self) -> Tuple[int, int]:
        """Find the position of the blank tile (0)."""
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    return (i, j)
        raise ValueError("No blank tile found in puzzle")
    
    def get_possible_moves(self) -> List['PuzzleState']:
        """Generate all possible moves from current state."""
        moves = []
        row, col = self.blank_pos
        
        # Define possible directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Check if move is within bounds
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                # Create new state by swapping blank with adjacent tile
                new_grid = deepcopy(self.grid)
                new_grid[row][col], new_grid[new_row][new_col] = \
                    new_grid[new_row][new_col], new_grid[row][col]
                
                moves.append(PuzzleState(new_grid))
        
        return moves
    
    def __eq__(self, other) -> bool:
        """Check if two puzzle states are equal."""
        if not isinstance(other, PuzzleState):
            return False
        return self.grid == other.grid
    
    def __hash__(self) -> int:
        """Make PuzzleState hashable for use in sets."""
        return hash(tuple(tuple(row) for row in self.grid))
    
    def __str__(self) -> str:
        """String representation of the puzzle state."""
        result = ""
        for row in self.grid:
            result += " ".join(str(cell) if cell != 0 else "*" for cell in row) + "\n"
        return result.strip()
    
    def to_tuple(self) -> Tuple:
        """Convert grid to tuple for hashing and comparison."""
        return tuple(tuple(row) for row in self.grid)