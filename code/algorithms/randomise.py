# Rembrand Ruppert, Mercedez van der Wal, Yessin Radouane
# Random Walk Algorithm (RWA) (3 directions possible every step / max coordinates based on district size / no overlaying cables (two segments with the same begin and ending coords))

import random

def random_assignment(houses, batteries):
    """
    Randomly assign each house to a battery
    """
    
    connections = {}

    # Assign random battery to each house
    for house in houses:
        random_battery = random.choice(batteries)
        connections[house] = random_battery
    
    return connections
    
def random_walk(start_position, end_position):
    """
    Random walk genereates the route per connection
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
            