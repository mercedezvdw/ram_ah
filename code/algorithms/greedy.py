# Rembrand Ruppert, Mercedez van der Wal, Yessin Radouane
# Random Walk Algorithm (RWA) (3 directions possible every step / max coordinates based on district size / no overlaying cables (two segments with the same begin and ending coords))
# choose random battery from every house and get a greedy path.
# Baseline 1.0

import random
import math


def calculate_distance(self, c1, c2):
    """
    Calculate the Manhattan distance between two coordinates
    """
    distance = abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])
    return distance
    
def make_connections(houses: dict, batteries: dict):
    """
    Connect the houses to the closest battery
    """
    connections = {}
    
    # Connect every house to a random battery
    for house_num, house in houses.items():        
        all_batteries = list(batteries.values())
        choice = random.choice(all_batteries)
        
        connections[house] = choice
    
    return connections

def check_logical_moves(current_position, end_position, illegal_move = None):
    """ This function checks which move minimizes the distance to the end position and returns that move.
        illegal_move is the move that is not allowed to be made, this is the move that will undo the previous move."""

    all_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    

    if illegal_move != None:
        all_moves.remove(illegal_move)

    # Possible moves
    move_1 = all_moves[0]
    move_2 = all_moves[1]
    move_3 = all_moves[2]

    # Calculate distance to end position after simulating the move
    new_position_1 = [current_position[0] + move_1[0], current_position[1] + move_1[1]]
    new_position_2 = [current_position[0] + move_2[0], current_position[1] + move_2[1]]
    new_position_3 = [current_position[0] + move_3[0], current_position[1] + move_3[1]]

    # Caclulate new distance from new position
    distance_1 = calculate_distance(new_position_1, end_position)
    distance_2 = calculate_distance(new_position_2, end_position)
    distance_3 = calculate_distance(new_position_3, end_position)

    distances = [distance_1, distance_2, distance_3]

    # Remove the move that adds the most distance to the end position
    if distance_1 == max(distances):
        all_moves.remove(move_1)

        if distance_2 > distance_3:
            all_moves.remove(move_2)
        else:
            all_moves.remove(move_3)
        
    elif distance_2 == max(distances):
        all_moves.remove(move_2)

        if distance_1 > distance_3:
            all_moves.remove(move_1)
        else:
            all_moves.remove(move_3)

    elif distance_3 == max(distances):
        all_moves.remove(move_3)
        if distance_1 > distance_2:
            all_moves.remove(move_1)
        else:
            all_moves.remove(move_2)

    return all_moves
    
def generate_routes(start_position, end_position):
    """
    Greedy walk generates the route per connection
    current pos: tuple
    end pos: list
    """
    current_position = start_position
    route = [current_position]
    last_direction = None
    inefficient_moves = {(0, 1): (0, -1), (0, -1): (0, 1), (1, 0): (-1, 0), (-1, 0): (1, 0)}
    
    while current_position != end_position:

        if last_direction == None:
            logical_moves = check_logical_moves(current_position, end_position)
            direction = random.choice(logical_moves)
            last_direction = direction
        
            
        elif last_direction == (0, 1):
            logical_moves = check_logical_moves(current_position, end_position, (0, -1))
            direction = random.choice(logical_moves)
            last_direction = direction
        
        elif last_direction == (0, -1):
            logical_moves = check_logical_moves(current_position, end_position, (0, 1))
            direction = random.choice(logical_moves)
            last_direction = direction

        elif last_direction == (1, 0):
            logical_moves = check_logical_moves(current_position, end_position, (-1, 0))
            direction = random.choice(logical_moves)
            last_direction = direction

        elif last_direction == (-1, 0):
            logical_moves = check_logical_moves(current_position, end_position, (1, 0))
            direction = random.choice(logical_moves)
            last_direction = direction

        if direction == inefficient_moves[last_direction]:
            print("WARNING: Inefficient move")

        # Calculate new position after following direction
        new_position = [current_position[0] + direction[0], current_position[1] + direction[1]]

        # Make sure it's within the grid size
        if 0 <= new_position[0] < 50 and 0 <= new_position[1] < 50:
            current_position = new_position
            route.append(current_position)
        
    return route