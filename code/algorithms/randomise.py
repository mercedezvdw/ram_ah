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