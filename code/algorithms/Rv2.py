# Rembrand Ruppert, Mercedez van der Wal, Yessin Radouane
# Random Walk Algorithm (RWA) (3 directions possible every step / max coordinates based on district size / no overlaying cables (two segments with the same begin and ending coords))
# choose random battery from every house and get a random but not least optimal path.

import random
import math
import numpy as np
from code.classes.cable import CableSegment


class Rv2():

    def __init__(self, batteries, houses):
        self.batteries = batteries
        self.houses = houses


    def calculate_distance(self, c1, c2):
        """
        Calculate the distance between two coordinates
        """
        distance = math.sqrt(((c1[0] - c2[0]) ** 2) + ((c1[1] - c2[1]) ** 2))
        return distance
        
    def make_connections(self):
        """
        Connect the houses to the closest battery
        """
        houses = self.houses
        batteries = self.batteries
        connections = {}
        
        
        #Cnnnect every house to a random battery
        for house_num, house in houses.items():        
            all_batteries = list(batteries.values())
            choice = random.choice(all_batteries)
            
            connections[house] = choice
            choice.capacity -= house.max_output
        
        return connections


    def check_logical_moves(self, current_position, end_position, illegal_move = None):
        """ This function checks which move adds the most distance to the end position and returns the other two moves.
            illegal_move is the move that is not allowed to be made, this is the move that will undo the previous move."""

        all_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        

        if illegal_move != None:
            all_moves.remove(illegal_move)

        # possible moves
        move_1 = all_moves[0]
        move_2 = all_moves[1]
        move_3 = all_moves[2]

        # calculate distance to end position after simulating the move
        new_position_1 = [current_position[0] + move_1[0], current_position[1] + move_1[1]]
        new_position_2 = [current_position[0] + move_2[0], current_position[1] + move_2[1]]
        new_position_3 = [current_position[0] + move_3[0], current_position[1] + move_3[1]]

        # caclulate new distance from new position
        distance_1 = self.calculate_distance(new_position_1, end_position)
        distance_2 = self.calculate_distance(new_position_2, end_position)
        distance_3 = self.calculate_distance(new_position_3, end_position)

        distances = [distance_1, distance_2, distance_3]

        # remove the move that adds the most distance to the end position
        if distance_1 == max(distances):
            all_moves.remove(move_1)
            
        elif distance_2 == max(distances):
            all_moves.remove(move_2)

        elif distance_3 == max(distances):
            all_moves.remove(move_3)


        return all_moves




        
    def generate_routes(self, start_position, end_position):
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

            if last_direction == None:
                logical_moves = self.check_logical_moves(current_position, end_position)
                direction = random.choice(logical_moves)
                last_direction = direction
            
                
            elif last_direction == (0, 1):
                logical_moves = self.check_logical_moves(current_position, end_position, (0, -1))
                direction = random.choice(logical_moves)
                last_direction = direction
            
            elif last_direction == (0, -1):
                logical_moves = self.check_logical_moves(current_position, end_position, (0, 1))
                direction = random.choice(logical_moves)
                last_direction = direction

            elif last_direction == (1, 0):
                logical_moves = self.check_logical_moves(current_position, end_position, (-1, 0))
                direction = random.choice(logical_moves)
                last_direction = direction

            elif last_direction == (-1, 0):
                logical_moves = self.check_logical_moves(current_position, end_position, (1, 0))
                direction = random.choice(logical_moves)
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
    

    def run(self):

        connections = self.make_connections()
        # print(f"Connections: {connections}\n\n")
        cables = {}
        cable_routes = {}

        for house, battery in connections.items():
            cables[house] = CableSegment(house.position, battery.position, 9)
            cable_routes[house] = self.generate_routes(house.position, battery.position)


            # print(f"cable_routes: {cable_routes}\n\n")
            # print(f"cables: {cables}\n\n")
        _sum = 0
        for house, route in cable_routes.items():
            _sum += len(route)

        total_cost = _sum * 9 + 5000 * len(self.batteries)
        print("Total cost: ", total_cost)
            # print(_sum)
            # result.append(_sum)

        # print("Average: ", (sum(result)/len(result))*9 + 25000)
        # print("Median: ", np.median(result)*9 + 25000)
        # print("Max: ", max(result)*9 + 25000)
        # print("Min: ", min(result)*9 + 25000)

        for num, battery in self.batteries.items():
            print(battery.capacity)

    
        adjusted_connections = {}
        house_idx = 0
        for house, battery in connections.items():
            adjusted_connections[house_idx] = [house.position, battery.position]
            house_idx += 1

        adjusted_cable_routes = {}
        cable_idx = 0
        for house, route in cable_routes.items():
            adjusted_cable_routes[cable_idx] = route
            cable_idx += 1

        # print(f"Connections {adjusted_connections}\n\n Cable routes {adjusted_cable_routes}\n\n Total cost {total_cost}")


        return adjusted_connections, adjusted_cable_routes, total_cost