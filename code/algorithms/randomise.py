# Rembrand Ruppert, Mercedez van der Wal, Yessin Radouane
# Random Walk Algorithm (RWA) (3 directions possible every step / max coordinates based on district size / no overlaying cables (two segments with the same begin and ending coords))

import random
import math

def calculate_distance(c1, c2):
    """
    Calculate the distance between two coordinates
    """
    distance = math.sqrt(((c1[0] - c2[0]) ** 2) + ((c1[1] - c2[1]) ** 2))
    
def make_connections(houses, batteries):
    """
    Connect the houses to the closest battery
    """
    connections = {}
    
    for house in houses:
        nearest_battery = None
        min_distance = None
        
        for battery in batteries:
                distance = calculate_distance(house.position, battery.position)
                if min_distance == None:
                    min_distance = distance
                elif distance < min_distance:
                    min_distance = distance
                    nearest_battery = battery
        
        connections[house] = nearest_battery
    
    return connections
    
def generate_routes(start_position, end_position):
    """
    Random walk generates the route per connection
    """
    
    current_position = start_position
    route = [current_position]
    
    while current_position != end_position:
        # Random choice of direction
        direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        
        # Calculate new position after following direction
        new_position = (current_position[0] + direction[0], current_position[1] + direction[1])

        # Make sure it's within the grid size
        if 0 <= new_position[0] < 50 and 0 <= new_position[1] < 50:
            current_position = new_position
            route.append(current_position)
        
    return route