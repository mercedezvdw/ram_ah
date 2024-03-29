# Mercedez van der Wal, Team RAM
# Nearest-Battery Heuristic Algorithm -- Shortest path to closest battery.
# For every house, check first if there is already a cable connected, to minimilize the costs of cables

import math
from random import sample
import random
import numpy as np
from code.classes.cable import CableSegment

class NBH_A():
    def __init__(self, batteries, houses, seed):
        self.batteries = batteries
        self.houses = houses
        random.seed(seed)


    def calculate_distance(self, c1, c2):
        """
        Calculate the Manhattan distance between two coordinates
        """
        distance = abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])
        return distance


    def check_battery_capacity(self, capacity, used_capacity, house_output):
        """
        Check if the battery has sufficient capacity to connect a certain house
        """
        capacity = capacity - used_capacity - house_output
        return capacity


    def find_cable_path(self, target_position, cable_routes, house_output):
        """
        Find the cable path of a coordinate and find the connected battery
        """
        for route in cable_routes.values():
            for coordinate in route:
                if coordinate == target_position:
                    destination = route[-1]
                    battery = self.find_battery(destination)
                    
                     # Make sure that the battery has sufficient capacity
                    if battery is not None:
                        check_capacity = self.check_battery_capacity(battery.capacity, battery.used_capacity, house_output)
                        if check_capacity > 0:
                            return battery

                
    def find_house(self, target_position):
        """
        Return house object related to given coordinate
        """
        for house in self.houses.values():
            if house.position == target_position:
                    return house


    def find_connection(self, cables, battery):
        """
        Find a connection with a given battery
        """
        for cable in cables.values():
            if cable.pos_end == battery.position:
                matching_house = cable.pos_begin
                return matching_house


    def find_cable_route(self, house_position, battery_position, cable_routes):
        """
        Find the coble route of a given house
        """
        for cable, route in cable_routes.items():
            if house_position in route:
                matching_cable = cable
                return matching_cable


    def undo_connection(self, house, battery, cable_routes, assign_again, connections):
        """
        Remove cable and undo connection of a given house and battery, make sure it will be reassigned
        """
        # Find index of the connection and cable route to remove them from the dictionaries
        matching_cable = self.find_cable_route(house.position, battery.position, cable_routes)
        del cable_routes[matching_cable]
        del connections[matching_cable]
        
        # Make sure to remove the output from the used capacity of battery and that the house will be reassigned again
        battery.remove_used_capacity(house.max_output)
        assign_again[matching_cable] = house
        
        return matching_cable
        
        
    def best_alternative(self):
        """
        Check which battery has biggest capacity left
        """
        bench = 0
        for battery in self.batteries.values():
            if battery.get_capacity() > bench:
                bench = battery.get_capacity()
                best_alternative = battery
                
        return best_alternative
        
                    
    def find_closest_battery(self, house, cable_routes, cables, assign_again, connections):
        """
        For each battery calculate the distance to find the closest battery
        """
        nearest_battery = None
        min_distance = float('inf')

        while nearest_battery is None:
            max_capacity = 0
            battery_full = None
            
            for i in range(len(self.batteries)):
                
                # Check if battery has sufficient capacity
                capacity = self.batteries[i].capacity - self.batteries[i].used_capacity
                used_capacity = capacity - house.max_output
                
                if capacity > max_capacity:
                    max_capacity = capacity
                    battery_full = self.batteries[i]
            
                if used_capacity > 0:
                    # Calculate distance and choose the battery with the closest distance
                    distance = self.calculate_distance(house.position, self.batteries[i].position)
                    if distance < min_distance:
                        min_distance = distance
                        nearest_battery = self.batteries[i]
                
            if nearest_battery is not None:
                return nearest_battery
            else:
                # If there is no battery left with sufficient capacity, undo random connection with battery that has most capacity left
                best_alternative = self.best_alternative()   
                random_house = self.find_connection(cables, best_alternative)
                random_house_object = self.find_house(random_house)
                
                self.undo_connection(random_house_object, best_alternative, cable_routes, assign_again, connections)
                
                # Reset min_distance for the next iteration
                min_distance = float('inf')


    def find_closest_cable(self, cable_routes, house_position, house_output, cables):
        """
        Find closest cable for a house to connect to
        """
        min_distance = float('inf')
        closest_cable = None
        connected_battery = None

        for route in list(cable_routes.values())[1:-1]:
            for coordinate in route:
                old_min_distance = min_distance
                distance = self.calculate_distance(house_position, coordinate)
                destination = route[-1]
                start_position = route[0]
                
                if distance < min_distance:
                    min_distance = distance
                    closest_cable = coordinate
                    
                    # Check if it's a battery and if it has sufficient capacity
                    battery = self.find_battery(closest_cable)
                    if battery is not None:
                        check_capacity = self.check_battery_capacity(battery.capacity, battery.used_capacity, house_output)
                        connected_battery = battery
                        if check_capacity > 0:
                            return closest_cable, connected_battery
                                
                    # If it is not a battery, find the connection to the battery
                    battery = self.find_battery(destination)
                    if battery is not None:
                        check_capacity = self.check_battery_capacity(battery.capacity, battery.used_capacity, house_output)
                        if check_capacity > 0:
                            connected_battery = battery
                            return closest_cable, connected_battery
                        else: 
                            min_distance = old_min_distance
                            closest_cable = None
                            connected_battery = None
                            continue       
                    
                    begin = destination
                    
                    # Keep going until you find the battery
                    for route in list(cable_routes.values()):
                        if route != []:
                            if begin == route[0]:
                                end = route[-1]
                                battery = self.find_battery(end)
                                if battery is not None:
                                    check_capacity = self.check_battery_capacity(battery.capacity, battery.used_capacity, house_output)
                                    if check_capacity > 0:
                                        connected_battery = battery
                                        return closest_cable, connected_battery
                                    else:
                                        min_distance = old_min_distance
                                        closest_cable = coordinate
                                        connected_battery = None
                                        break
                                else:
                                    begin = end
        return None, None


    def find_battery(self, target_position):
        for battery in self.batteries.values():
            if battery.position == target_position:
                    return battery


    def compare_results(self, house_position, pos1, pos2):
        """
        Compare the distance between two positions
        """
        distance1 = self.calculate_distance(house_position, pos1)
        distance2 = self.calculate_distance(house_position, pos2)
            
        if distance1 < distance2:
            return pos1
        else: 
            return pos2


    def check_if_house(self, cable_route):
        """
        Find house object in cable route
        """
        for route in cable_route[1:]:
            for house in self.houses.values():
                if house.position == route:
                    return house

    def create_cable_route(self, start_position, end_position, battery):
        """
        Create cable with shortest path (based on heuristics) from start to end position
        """
        steps_right = 0
        steps_left = 0
        steps_up = 0
        steps_down = 0
        current_position = start_position
        
        # Compare the x coordinates, to determine to go left or right
        if start_position[0] < end_position[0]:
            steps_right = end_position[0] - start_position[0]
        elif start_position[0] > end_position[0]:
            steps_left = start_position[0] - end_position[0]
        
        # Compare the y coordinates, to determine to go up or down
        if start_position[1] < end_position[1]:
            steps_up = end_position[1] - start_position[1]
        elif start_position[1] > end_position[1]:
            steps_down = start_position[1] - end_position[1]

        cable_route = [current_position.copy()]
        
        # Move on the y axis
        for i in range(steps_up):
            current_position = [current_position[0], current_position[1] + 1]
            cable_route.append(current_position.copy())
        for i in range(steps_down):
            current_position = [current_position[0], current_position[1] - 1]
            cable_route.append(current_position.copy())
        
        # Move on the x axis
        for i in range(steps_right):
            current_position = [current_position[0] + 1, current_position[1]]
            cable_route.append(current_position.copy())
        for i in range(steps_left):
            current_position = [current_position[0] - 1, current_position[1]]
            cable_route.append(current_position.copy())
            
        house = self.check_if_house(cable_route)
        
        if house is not None:
            check_capacity = self.check_battery_capacity(battery.capacity, battery.used_capacity, house.max_output)
    
        return cable_route     
                
    def run(self):
        """
        Execute Nearest Battery Heuristic Algorithm
        """
        cables = {}
        cable_routes = {}
        connections = {}
        sum_costs = 5000 * (len(self.batteries))
        assign_again = {}
        optimize = {}
        
        houses_copy = self.houses.copy()
        random.shuffle(houses_copy)
        
        for i in range(len(houses_copy)):
            # Check if there is already a cable path through this house
            path = self.find_cable_path(houses_copy[i].position, cable_routes, houses_copy[i].max_output)
            if path is not None:
                match = path.position
                closest_option = None
                route_costs = 0
                cable_route = [houses_copy[i].position]

            else:
                # Find closest battery with sufficient capacity
                closest_battery = self.find_closest_battery(houses_copy[i], cable_routes, cables, assign_again, connections)
                
                # Find the closest cable and which battery it is connected to
                closest_cable, connected_battery = self.find_closest_cable(cable_routes, houses_copy[i].position, houses_copy[i].max_output, cables)

                # If there is no cable to connect to, there comes a new cable to the closest battery
                if closest_cable is None:
                    closest_option = closest_battery.position
                    match = closest_battery.position
                    cable_route = self.create_cable_route(houses_copy[i].position, closest_battery.position, closest_battery)

                # Compare the closest cable and the closest battery to decide which option is more close
                else:
                    closest_option = self.compare_results(houses_copy[i].position, closest_battery.position, closest_cable)

                    # If the battery itself is closer, the cable will be connected to the closest battery
                    if closest_option == closest_battery.position:
                        match = closest_battery.position
                        cable_route = self.create_cable_route(houses_copy[i].position, closest_battery.position, closest_battery)

                    # If not, the connected battery is from the closest cable
                    else:
                        cable_route = self.create_cable_route(houses_copy[i].position, closest_option, connected_battery)
                        match = connected_battery.position
                
                route_costs = (len(cable_route) - 1) * 9
            
            cable_routes[i] = cable_route
            connections[i] = [houses_copy[i].position, match]
            cables[i] = CableSegment(houses_copy[i].position, match, route_costs)
            
            # Add capacity of house to used capacity of the connected battery
            battery = self.find_battery(match)
            battery.add_used_capacity(houses_copy[i].max_output)
        
        while len(assign_again) != 0: 
            for key, house in assign_again.copy().items():
                house = assign_again[key]
                
                # Check if there is already a cable path through this house
                path = self.find_cable_path(house.position, cable_routes, house.max_output)
                if path is not None:
                    match = path.position
                    closest_option = None
                    route_costs = 0
                    cable_route = [house.position]

                else:
                    # Find closest battery with sufficient capacity
                    closest_battery = self.find_closest_battery(house, cable_routes, cables, assign_again, connections)
                    
                    # Find the closest cable and which battery it is connected to
                    closest_cable, connected_battery = self.find_closest_cable(cable_routes, house.position, house.max_output, cables)

                    # If there is no cable to connect to, there comes a new cable to the closest battery
                    if closest_cable is None:
                        closest_option = closest_battery.position
                        match = closest_battery.position
                        cable_route = self.create_cable_route(house.position, closest_battery.position, closest_battery)

                    # Compare the closest cable and the closest battery to decide which option is more close
                    else:
                        closest_option = self.compare_results(house.position, closest_battery.position, closest_cable)

                        # If the battery itself is closer, the cable will be connected to the closest battery
                        if closest_option == closest_battery.position:
                            match = closest_battery.position
                            cable_route = self.create_cable_route(house.position, closest_battery.position, closest_battery)

                        # If not, the connected battery is from the closest cable
                        else:
                            cable_route = self.create_cable_route(house.position, closest_option, connected_battery)
                            match = connected_battery.position
                
                    route_costs = (len(cable_route) - 1) * 9
            
                cable_routes[key] = cable_route
                connections[key] = [house.position, match]
                cables[key] = CableSegment(house.position, match, route_costs)
            
                # Add capacity of house to used capacity of the connected battery
                battery = self.find_battery(match)
                battery.add_used_capacity(house.max_output)
                
                del assign_again[key]
    
        houses_shuffled = houses_copy

        # Add all the route costs to sum costs
        for route in cable_routes.values():
            route_costs = (len(route) - 1) * 9
            sum_costs += route_costs
        
        print(f"The total price of the cables is {sum_costs}")

        return sum_costs, cable_routes, connections, houses_shuffled