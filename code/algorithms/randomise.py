# Rembrand Ruppert, Mercedez van der Wal, Yessin Radouane
# Random Walk Algorithm (RWA) (3 directions possible every step / max coordinates based on district size / no overlaying cables (two segments with the same begin and ending coords))

import random
import math


def calculate_distance(c1, c2):
    """
    Calculate the distance between two coordinates
    """
    distance = math.sqrt(((c1[0] - c2[0]) ** 2) + ((c1[1] - c2[1]) ** 2))
    return distance
    
def make_connections(houses: dict, batteries: dict):
    """
    Connect the houses to the closest battery
    """
    connections = {}
    
    for house_num, house in houses.items():
        nearest_battery = None
        min_distance = 10e9
        
        for battery_num, battery in batteries.items():
                distance = calculate_distance(house.position, battery.position)
                # print(min_distance)

                if distance < min_distance:
                    # print("new smaller distance found")
                    min_distance = distance
                    nearest_battery = battery
                
                # print(min_distance)
        
        connections[house] = nearest_battery
    
    return connections
    
def generate_routes(start_position, end_position):
    """
    Random walk generates the route per connection
    current pos: tuple
    end pos: list
    """
    # print(f"Generating route from {start_position} to {end_position}")
    
    current_position = start_position
    route = [current_position]
    last_direction = None
    inefficient_moves = {(0, 1): (0, -1), (0, -1): (0, 1), (1, 0): (-1, 0), (-1, 0): (1, 0)}
    
    while current_position != end_position:

        # Random choice of direction
        # print(f"Current position: {current_position}")
        # print(last_direction)

        if last_direction == None:
            direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            last_direction = direction
        
        # else:
        #     choices = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        #     choices.remove(inefficient_moves[last_direction])
        #     direction = random.choice(choices)
        #     if direction == inefficient_moves[last_direction]:
        #         print("WARNING: Inefficient move")
        #     last_direction = direction
            
        elif last_direction == (0, 1):
            direction = random.choice([(0, 1), (1, 0), (-1, 0)])
            last_direction = direction
        
        elif last_direction == (0, -1):
            direction = random.choice([(0, -1), (1, 0), (-1, 0)])
            last_direction = direction

        elif last_direction == (1, 0):
            direction = random.choice([(0, 1), (0, -1), (1, 0)])
            last_direction = direction

        elif last_direction == (-1, 0):
            direction = random.choice([(0, 1), (0, -1), (-1, 0)])
            last_direction = direction

        if direction == inefficient_moves[last_direction]:
            print("WARNING: Inefficient move")

        
        # Calculate new position after following direction
        new_position = [current_position[0] + direction[0], current_position[1] + direction[1]]
        # print(new_position)

        # Make sure it's within the grid size
        if 0 <= new_position[0] < 50 and 0 <= new_position[1] < 50:
            current_position = new_position
            route.append(current_position)
        
    return route