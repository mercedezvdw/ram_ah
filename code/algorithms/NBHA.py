# Mercedez van der Wal, Rembrand Ruppert
# Nearest-Battery Heuristic Algorithm -- Shortest path to closest battery.
# For every house, check first if there is already a cable connected, to minimilize the costs of cables

import math
import random
import numpy as np
from code.classes.cable import CableSegment

class NBH_A():
    def __init__(self, batteries, houses):
        self.batteries = batteries
        self.houses = houses


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
                
                    if battery is not None:
                        check_capacity = self.check_battery_capacity(battery.capacity, battery.used_capacity, house_output)
                        if check_capacity > 0:
                            return battery

                
    def find_house(self, target_position):
        for house in self.houses.values():
            if house.position == target_position:
                    return house
        return None

    def find_connection(self, cables, battery):
        """
        Find a connection with a given battery
        """
        matching_house = None
        for cable in cables.values():
            if cable.pos_end == battery.position:
                matching_house = cable.pos_begin
                return matching_house

    def find_cable_route(self, house_position, battery_position, cable_routes):
        for cable, route in cable_routes.items():
            if house_position in route:
                matching_cable = cable
                return matching_cable

    def undo_connection(self, house, battery, cable_routes, assign_again):
        matching_cable = self.find_cable_route(house.position, battery.position, cable_routes)
        del cable_routes[matching_cable]
        battery.remove_used_capacity(house.max_output)
        assign_again.append(house)
        
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
        
                    
    def find_closest_battery(self, house, cable_routes, cables, assign_again):
        """
        For each battery calculate the distance to find the closest battery
        """
        nearest_battery = None
        min_distance = float('inf')

        
        while True:
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
                
                self.undo_connection(random_house_object, best_alternative, cable_routes, assign_again)
                
                # Reset min_distance for the next iteration
                min_distance = float('inf')


    def find_closest_cable(self, cable_routes, house_position, house_output, cables):
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


    def find_connected_battery(self, cables, closest_cable):
        for cable in cables.values():
            if cable.pos_begin == closest_cable:
                connected_battery = cable.pos_end
                return connected_battery
        return None


    def find_battery(self, target_position):
        for battery in self.batteries.values():
            if battery.position == target_position:
                    return battery
        return None


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
            if check_capacity < 0:
                AssertionError
    
        return cable_route

    def reset_batteries(self):
        for i in range(len(self.batteries)):
            self.batteries[i].reset_capacity()
            
    def find_closest_coordinate(self, target_coordinate, cable_route):
        closest_coordinate = None
        min_distance = float('inf')
        
        for coordinate in cable_route:
            distance = calculate_distance(target_coordinate, coordinate)
            if distance < min_distance:
                min_distance = distance
                closest_coordinate = coordinate
        
        return closest_coordinate
                
    def get_result(self):
        """
        Execute Nearest Battery Heuristic Algorithm
        """
        cables = {}
        cable_routes = {}
        connections = {}
        sum_costs = 5000 * (len(self.batteries))
        assign_again = []
        
        # Reset the battery capacacities
        self.reset_batteries()
        
        houses_copy = self.houses.copy()
        # random.shuffle(houses_copy)
        
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
                closest_battery = self.find_closest_battery(houses_copy[i], cable_routes, cables, assign_again)
                
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
            sum_costs += route_costs
            
            # Add capacity of house to used capacity of the connected battery
            battery = self.find_battery(match)
            battery.add_used_capacity(houses_copy[i].max_output)
        
        j = 150
        
        while len(assign_again) != 0: 
            for i in range(len(assign_again)):
                house = assign_again[i]
                
                # Check if there is already a cable path through this house
                path = self.find_cable_path(house.position, cable_routes, house.max_output)
                if path is not None:
                    match = path.position
                    closest_option = None
                    route_costs = 0
                    cable_route = [houses_copy[i].position]

                else:
                    # Find closest battery with sufficient capacity
                    closest_battery = self.find_closest_battery(house, cable_routes, cables, assign_again)
                    
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
            
                cable_routes[j+i] = cable_route
                connections[j+i] = [house.position, match]
                cables[j+i] = CableSegment(house.position, match, route_costs)
                sum_costs += route_costs
            
                # Add capacity of house to used capacity of the connected battery
                battery = self.find_battery(match)
                battery.add_used_capacity(house.max_output)
                
                assign_again.pop(i)
                
        # Make sure all houses are assigned and connected to a battery
        if assign_again == []:
            return cables, cable_routes, sum_costs, connections
    
    def run(self):
        """
        Execute Nearest Battery Heuristic Algorithm
        """
        result = []
        min_costs = float('inf')
        min_cables = None
        min_cable_routes = None
        
        # Run 1000 iterations
        for i in range(1):
            cables, cable_routes, sum_costs, connections = self.get_result()
            result.append(sum_costs)
            
            # Plot the best iteration
            if sum_costs < min_costs:
                min_cable_routes = cable_routes
        
        print("Average: ", (sum(result)/len(result)))
        print("Median: ", np.median(result))
        print("Max: ", max(result))
        print("Min: ", min(result))

        return sum_costs, min_cable_routes, connections
        