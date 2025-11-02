"""
CS170 Project 1: 8-Puzzle Solver

Authors: Shreyas, Rishith, Rehan
"""

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
