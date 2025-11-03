"""
CS170 Project 1: 8-Puzzle Solver

Authors: Shreyas, Rishith, Rehan
"""

import math
from typing import List, Tuple, Optional
from copy import deepcopy

class Node:
    """Represents a state in the search tree"""
    def __init__(self, state, parent=None, action=None, depth=0, cost=0):
        self.state = state  # The puzzle configuration
        self.parent = parent  # Parent node
        self.action = action  # Action that led to this state
        self.depth = depth  # Depth in the search tree (g(n))
        self.cost = cost  # Total cost f(n) = g(n) + h(n)
    
    def __lt__(self, other):
        """Comparison for priority queue"""
        return self.cost < other.cost
    
    def __eq__(self, other):
        """Check if two nodes have the same state"""
        return self.state == other.state
    
    def __hash__(self):
        """Make node hashable for visited set"""
        return hash(str(self.state))

class Problem:
    """Represents the Eight-Puzzle problem"""
    def __init__(self, initial_state, goal_state=None):
        self.initial_state = initial_state
        self.goal_state = goal_state if goal_state else [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.operators = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    
    def is_goal(self, state):
        """Check if state is the goal state"""
        return state == self.goal_state
    
    def find_blank(self, state):
        """Find the position of the blank (0) in the puzzle"""
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return i, j
        return None

    def get_successors(self, state):
        """Generate all valid successor states"""
        successors = []
        blank_row, blank_col = self.find_blank(state)
        # Possible moves: LEFT, RIGHT, UP, DOWN
        moves = {
            'LEFT': (0, -1),
            'RIGHT': (0, 1),
            'UP': (-1, 0),
            'DOWN': (1, 0)
        }
        
        for action, (dr, dc) in moves.items():
            new_row, new_col = blank_row + dr, blank_col + dc
            
            # Check if move is valid
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                # Create new state by swapping blank with adjacent tile
                new_state = deepcopy(state)
                new_state[blank_row][blank_col] = new_state[new_row][new_col]
                new_state[new_row][new_col] = 0
                
                successors.append((new_state, action))
        
        return successors


    def misplaced_tile_heuristic(self, state):
        """Count number of misplaced tiles (excluding blank)"""
        misplaced = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != 0 and state[i][j] != self.goal_state[i][j]:
                    misplaced += 1
        return misplaced
    
    def euclidean_distance_heuristic(self, state):
        """Calculate Euclidean distance of tiles from goal positions"""
        distance = 0 # Initialize the total distance to 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != 0: # Skip 0 because it does not need to move towards any goal tile
                    value = state[i][j] # The tile number (1-8)
                    goal_row = (value - 1) // 3 # To find goal row
                    goal_col = (value - 1) % 3 # To find goal column
                    
                    distance += math.sqrt((i - goal_row)**2 + (j - goal_col)**2) # Calculate Euclidean distance
    
        return distance
