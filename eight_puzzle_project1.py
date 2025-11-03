"""
CS170 Project 1: 8-Puzzle Solver

Authors: Shreyas, Rishabh, Rehan
"""

import math
import heapq
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

def print_state(state):
    """Print the puzzle state in a readable format"""
    for row in state: # Loop through each row
        # If the tile value is 0, replace it with b to show a blank space
        # Otherwise convert the tile number to a string to create a list of string values
        # Join the values of the list to create the row with spaces in between
        print(' '.join(['b' if x == 0 else str(x) for x in row]))


def general_search(problem, heuristic='uniform'):
    """
    General A* search algorithm
    heuristic options: 'uniform', 'misplaced', 'euclidean'
    """
    # Final values
    nodes_expanded = 0
    max_queue_size = 0
    
    # Choose heuristic function
    if heuristic == 'uniform':
        h_func = lambda state: 0
    elif heuristic == 'misplaced':
        h_func = problem.misplaced_tile_heuristic
    elif heuristic == 'euclidean':
        h_func = problem.euclidean_distance_heuristic
    else:
        raise ValueError("Invalid heuristic")
    
    # Initialize
    initial_h = h_func(problem.initial_state)
    initial_node = Node(problem.initial_state, None, None, 0, initial_h)
    
    frontier = [initial_node]  # Priority queue
    heapq.heapify(frontier)
    
    visited = set()  # To avoid revisiting states
    
    # Print initial state
    print("\nExpanding state")
    print_state(problem.initial_state)
    print()

    while frontier:
        # Track max queue size
        max_queue_size = max(max_queue_size, len(frontier))
        
        # Get node with lowest f(n) = g(n) + h(n)
        current_node = heapq.heappop(frontier) # Use heapq.heappop to find the lowest value in O(log n) time
        
        # Convert state to tuple for hashing
        state_tuple = tuple(tuple(row) for row in current_node.state)
        
        # Skip if already visited
        if state_tuple in visited:
            continue
        
        visited.add(state_tuple)
        
        # Check if goal
        if problem.is_goal(current_node.state):
            print("Goal!!!")
            print()
            print(f"To solve this problem the search algorithm expanded a total of {nodes_expanded} nodes.")
            print(f"The maximum number of nodes in the queue at any one time: {max_queue_size}.")
            print(f"The depth of the goal node was {current_node.depth}.")
            
            # Return solution path
            return reconstruct_path(current_node), nodes_expanded, max_queue_size
        
        # Expand node
        nodes_expanded += 1
        
        for successor_state, action in problem.get_successors(current_node.state):
            successor_tuple = tuple(tuple(row) for row in successor_state)
            
            if successor_tuple not in visited:
                g_n = current_node.depth + 1  # Cost from start
                h_n = h_func(successor_state)  # Heuristic
                f_n = g_n + h_n  # Total cost
                
                successor_node = Node(successor_state, current_node, action, g_n, f_n)
                heapq.heappush(frontier, successor_node)
        
        # After expanding, show the best state to expand next
        if frontier:
            # Peek at the best node without removing it
            best_node = min(frontier)
            g_n = best_node.depth
            h_n = best_node.cost - best_node.depth
            
            # Format h(n) - show as int if it's a whole number, otherwise 1 decimal
            if h_n == int(h_n):
                h_n_str = str(int(h_n))
            else:
                h_n_str = f"{h_n:.1f}"
            
            print(f"The best state to expand with g(n) = {g_n} and h(n) = {h_n_str} is...")
            print_state(best_node.state)
            print("Expanding this node...")
            print()
    
    print("No solution found!")
    return None, nodes_expanded, max_queue_size


def reconstruct_path(node):
    """Reconstruct the solution path from goal to start"""
    path = []
    current = node
    while current.parent is not None:
        path.append((current.action, current.state))
        current = current.parent
    path.reverse()
    return path


def is_solvable(state):
    """Check if puzzle is solvable using inversion count"""
    # Flatten the puzzle, excluding the blank
    flat = [val for row in state for val in row if val != 0]
    
    # Count inversions
    inversions = 0
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inversions += 1
    
    # Puzzle is solvable if inversions are even
    return inversions % 2 == 0

def get_user_input():
    """Get puzzle configuration from user"""
    print("Welcome to Rishabh, Rehan, and Shreyas's 8 puzzle solver.")  # Display a welcome message
    print('Type "1" to use a default puzzle, or "2" to enter your own puzzle.') # Prompt the user for input options
    
    choice = input().strip() # Read the user's choice and remove the whitespace
    
    if choice == '1': # Option 1 is using a default puzzle
        initial_state = [[1, 2, 3], [4, 8, 0], [7, 6, 5]]
    else: # Option 2 is the user inputs his own puzzle
        print("\nEnter your puzzle, use a zero to represent the blank")
        initial_state = [] # Initialize an empty list to store the three puzzle rows
        
        # Each input line is split into numbers, converted to integers, and added to the state
        row1 = input("Enter the first row, use space or tabs between numbers ")
        initial_state.append([int(x) for x in row1.split()])
        
        row2 = input("Enter the second row, use space or tabs between numbers ")
        initial_state.append([int(x) for x in row2.split()])
        
        row3 = input("Enter the third row, use space or tabs between numbers ")
        initial_state.append([int(x) for x in row3.split()])
    
    # After puzzle input, ask the user which algorithm they want to use
    print("\nEnter your choice of algorithm")
    print("1. Uniform Cost Search")
    print("2. A* with the Misplaced Tile heuristic.")
    print("3. A* with the Euclidean distance heuristic.")
    print()
    
    # Read the user's selection
    algo_choice = input().strip()
    
    # Map the number choice to the algorithm name
    heuristic_map = {
        '1': 'uniform', # Uniform cost search
        '2': 'misplaced', # A* using number of misplaced tiles
        '3': 'euclidean' # A* using Euclidean distance heuristic
    }
    
    # Get the number chosen by the user and make "uniform" the default choice
    heuristic = heuristic_map.get(algo_choice, 'uniform')
    
    # Returns the puzzle configuration chosen and the heuristic that was chosen
    return initial_state, heuristic

def main():
    """Main function"""
    # Get user input
    initial_state, heuristic = get_user_input()
    
    # Check if puzzle is solvable
    if not is_solvable(initial_state):
        print("\nThis puzzle is not solvable! Please try a different initial state.")
        return
    
    # Create problem instance
    problem = Problem(initial_state)
    
    # Run search
    solution, nodes_expanded, max_queue = general_search(problem, heuristic)
    
    # Optional: Print solution path (extra credit)
    if solution and len(solution) > 0:
        print("\n" + "="*50)
        print("Solution Path (Extra Credit):")
        print("="*50)
        print("\nInitial State:")
        print_state(problem.initial_state)
        
        for i, (action, state) in enumerate(solution):
            print(f"\nStep {i+1}: {action}")
            print_state(state)

if __name__ == "__main__":
    main()