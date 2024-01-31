# Yessin Radouane, Team RAM
# Depth First Mycelium Algorithm (DFM) (Finds furthest house from battery and the house furthest from that house, connects them with a cable, then connects the rest of the houses to the closest cable or battery)

import math
from matplotlib import pyplot as plt
import numpy as np
import random
from itertools import combinations

class DFM():

    def __init__(self, batteries, houses, seed):
        self.batteries = batteries
        self.houses = houses
        self.furthest_house = {}
        self.furthest_from_furthest_house = {}
        random.seed(seed)


    def calculate_distance(self, c1, c2):
        """
        Calculate the Manhattan distance between two coordinates
        """
        distance = abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])
        return distance
    

    def connect_house(self, house, battery, connections):
        """Connect a house to a battery."""
        if battery not in connections:
            connections[battery] = []
        connections[battery].append(house)
        battery.capacity -= house.max_output


    def disconnect_house(self, house, battery, connections):
        """Disconnect a house from a battery."""
        connections[battery].remove(house)
        battery.capacity += house.max_output


    def switch_houses(self, house_to_disconnect, house_to_connect, battery, alt_battery, connections):
        """Switch a house from one battery to another."""
        connections[battery].remove(house_to_disconnect)
        battery.capacity += house_to_disconnect.max_output
        self.connect_house(house_to_connect, alt_battery, connections)


    def find_key_by_value(self, house_object):
        for key, value in self.houses.items():
            if value == house_object:
                return key
        return None


    def get_connections(self):
        connections = {}
        distances = {}
        unconnected_houses = set(self.houses.keys())

        # Calculate distance from house to each battery and sort batteries by distance for each house
        for house_num, house in self.houses.items():
            distances[house] = sorted(
                self.batteries.items(),
                key=lambda item: self.calculate_distance(house.position, item[1].position)
            )

        # Initial connection attempt
        for house_num, house in self.houses.items():
            for battery_num, battery in distances[house]:
                if battery.capacity >= house.max_output:
                    self.connect_house(house, battery, connections)
                    unconnected_houses.remove(house_num)
                    break

        while len(unconnected_houses) > 0:            
            # Check for simple change
            for unconnected_house in list(unconnected_houses):

                for house_num, house in self.houses.items():
                    if house_num == unconnected_house:
                        unconnected_house = house
                        unconnected_house_num = house_num

                # Find battery with most capacity left:
                max_capacity = 0
                max_capacity_battery = None
                for battery in self.batteries.values():
                    if battery.capacity > max_capacity:
                        max_capacity = battery.capacity
                        max_capacity_battery = battery

                # Find battery with second most capacity left:
                second_max_capacity = 0
                second_max_capacity_battery = None
                for battery in self.batteries.values():
                    if battery.capacity > second_max_capacity and battery != max_capacity_battery:
                        second_max_capacity = battery.capacity
                        second_max_capacity_battery = battery

                # Loop over houses in first battery connections
                for house in connections[max_capacity_battery]:

                    max_output = house.max_output
                    # print(f"Checking: {max_output} < {second_max_capacity} and {unconnected_house.max_output} < {max_capacity + max_output}")
                    if max_output < second_max_capacity and unconnected_house.max_output < max_capacity + max_output:

                        # Disconnect house
                        connections[max_capacity_battery].remove(house)
                        max_capacity_battery.capacity += max_output
                        
                        # Connect house to second battery
                        connections[second_max_capacity_battery].append(house)
                        second_max_capacity_battery.capacity -= max_output

                        # Connect unconnected house to first battery
                        connections[max_capacity_battery].append(unconnected_house)
                        max_capacity_battery.capacity -= unconnected_house.max_output
                        unconnected_houses.remove(unconnected_house_num)
                        break

                # Check for more complex change over all batteries
                if len(unconnected_houses) > 0:
                    all_bateries = [battery for battery in connections.keys()]

                    # Loop over every combination of batteries
                    battery_combinations = list(combinations(all_bateries, 2))

                    # Boolean to check if a change has been made
                    changed = False
                    
                    # Loop over every combination of batteries
                    for battery_1, battery_2 in battery_combinations:
                        # print(f"Checking batteries {battery_1} and {battery_2}")

                        if changed:
                            break

                        # Loop over every house in battery 1
                        for house_b1 in connections[battery_1]:

                            if changed:
                                break

                            # Loop over every house in battery 2
                            for house_b2 in connections[battery_2]:

                                if changed:
                                    break

                                # Simulate capacities in case of switch houses
                                new_b1_capacity = battery_1.capacity + house_b1.max_output - house_b2.max_output
                                new_b2_capacity = battery_2.capacity + house_b2.max_output - house_b1.max_output

                                # Check if switch is possible
                                if new_b1_capacity >= 0 and new_b2_capacity >= 0:
                                    
                                    # check if unconnected house can be added to first battery in case of switch
                                    if new_b1_capacity >= unconnected_house.max_output:

                                        # Switch can be made
                                        # print("Switching houses")
                                        connections[battery_1].remove(house_b1)
                                        connections[battery_1].append(house_b2)
                                        connections[battery_2].remove(house_b2)
                                        connections[battery_2].append(house_b1)

                                        battery_1.capacity += house_b1.max_output - house_b2.max_output
                                        battery_2.capacity += house_b2.max_output - house_b1.max_output

                                        # Connect unconnected house to battery 1
                                        connections[battery_1].append(unconnected_house)
                                        battery_1.capacity -= unconnected_house.max_output
                                        unconnected_houses.remove(unconnected_house_num)
                                        changed = True
                                        break

                                    # check if unconnected house can be added to second battery in case of switch
                                    elif new_b2_capacity >= unconnected_house.max_output:

                                        # Switch can be made
                                        # print("Switching houses")
                                        connections[battery_1].remove(house_b1)
                                        connections[battery_1].append(house_b2)
                                        connections[battery_2].remove(house_b2)
                                        connections[battery_2].append(house_b1)

                                        battery_1.capacity += house_b1.max_output - house_b2.max_output
                                        battery_2.capacity += house_b2.max_output - house_b1.max_output

                                        # Connect unconnected house to battery 2
                                        connections[battery_2].append(unconnected_house)
                                        battery_2.capacity -= unconnected_house.max_output
                                        unconnected_houses.remove(unconnected_house_num)
                                        changed = True

                                        break
                                        
        # Print unconnected houses
        if unconnected_houses:
            print(f"Unconnected houses: {unconnected_houses}")
            for house in unconnected_houses:
                print(f"House {house} at {self.houses[house].position} with max output {self.houses[house].max_output} could not be connected")
        else:
            print("All houses successfully connected")

        return connections
    

    def check_best_move(self, current_position, end_position, illegal_move = None):
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
        distance_1 = self.calculate_distance(new_position_1, end_position)
        distance_2 = self.calculate_distance(new_position_2, end_position)
        distance_3 = self.calculate_distance(new_position_3, end_position)

        distances = [distance_1, distance_2, distance_3]

        best_move = None

        # Remove the move that adds the most distance to the end position
        if distance_1 == min(distances):
            best_move = move_1
            
        elif distance_2 == min(distances):
            best_move = move_2

        elif distance_3 == min(distances):
            best_move = move_3

        return best_move

        
    def generate_routes(self, start_position, end_position):
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
                best_move = self.check_best_move(current_position, end_position)
                last_direction = best_move
                
            elif last_direction == (0, 1):
                best_move = self.check_best_move(current_position, end_position, (0, -1))
                last_direction = best_move
            
            elif last_direction == (0, -1):
                best_move = self.check_best_move(current_position, end_position, (0, 1))
                last_direction = best_move

            elif last_direction == (1, 0):
                best_move = self.check_best_move(current_position, end_position, (-1, 0))
                last_direction = best_move

            elif last_direction == (-1, 0):
                best_move = self.check_best_move(current_position, end_position, (1, 0))
                last_direction = best_move
            
            # Calculate new position after following direction
            new_position = [current_position[0] + best_move[0], current_position[1] + best_move[1]]

            # Make sure it's within the grid size
            if 0 <= new_position[0] <= 50 and 0 <= new_position[1] <= 50:
                current_position = new_position
                route.append(current_position)

        return route
        

    def set_cables(self, connections):
        routes = {}
    
        # Create base cables for furthest house and furthest house from this house
        for battery in connections.keys():
            furthest_house = None
            longest_distance = 0
            furthest_from_furthest_house = None
            second_distance = 0

            for house in connections[battery]:
                distance = self.calculate_distance(battery.position, house.position)
                if distance > longest_distance:
                    longest_distance = distance
                    furthest_house = house

            for house in connections[battery]:
                distance = self.calculate_distance(furthest_house.position, house.position)
                if distance > second_distance and house != furthest_house:
                    second_distance = distance
                    furthest_from_furthest_house = house

            furthest_route = self.generate_routes(battery.position, furthest_house.position)
            second_furthest_route = self.generate_routes(battery.position, furthest_from_furthest_house.position)
        
            routes[battery] = {}
            routes[battery][furthest_house] = furthest_route
            routes[battery][furthest_from_furthest_house] = second_furthest_route

            self.furthest_house[battery] = furthest_house
            self.furthest_from_furthest_house[battery] = furthest_from_furthest_house

        # Now to connect the rest of the houses per battery
        # Go depth first, so find the furthes house and connect to closest cable or linked battery
        for battery in connections.keys():
            ununconnected_houses = [house for house in connections[battery] if house not in [self.furthest_house[battery], self.furthest_from_furthest_house[battery]]]
               
            # Find furthest house from battery and make routes until all houses are connected
            while len(ununconnected_houses) > 0:
                furthest_house = None
                longest_distance = 0
                for house in ununconnected_houses:
                    distance = self.calculate_distance(battery.position, house.position)
                    if distance > longest_distance:
                        longest_distance = distance
                        furthest_house = house
    
                # Find closest cable or linked battery
                smallest_distance_cable = 1e9
                distance_battery = None
                closest_cable = None
                for route in routes[battery].values():

                    # Find closest cable
                    for cable in route:
                        distance = self.calculate_distance(cable, furthest_house.position)
                        if distance < smallest_distance_cable:
                            smallest_distance_cable = distance
                            closest_cable = cable

                # fFind closest battery
                distance_battery = self.calculate_distance(battery.position, furthest_house.position)

                if distance_battery < smallest_distance_cable:
                    # Connect to battery
                    route = self.generate_routes(battery.position, furthest_house.position)

                    # Add route to routes
                    routes[battery][furthest_house] = route

                    # remove house from unconnected houses
                    ununconnected_houses.remove(furthest_house)

                else:
                    # Connect to closest cable
                    route = self.generate_routes(closest_cable, furthest_house.position)

                    # Add route to routes
                    routes[battery][furthest_house] = route

                    # Remove house from unconnected houses
                    ununconnected_houses.remove(furthest_house)
                        
        return routes


    def DrawCase(self, connections, routes, extraGridSpace = 2):
        # Define colors for each battery
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

        idx = 0
        for battery, houses in connections.items():
            # Assign color to the current battery and its houses
            color = colors[idx % len(colors)]

            # Plot houses
            for house in houses:
                plt.scatter(house.position[0], house.position[1], s=75, color=color, marker='^', label='House', zorder=1)

            # Plot battery
            plt.scatter(battery.position[0], battery.position[1], s=75, color=color, marker='s', label='Battery', zorder=1)

            # Plot cables
            if battery in routes:
                for route_key in [self.furthest_house[battery], self.furthest_from_furthest_house[battery]]:
                    if route_key in routes[battery]:
                        route = routes[battery][route_key]
                        x, y = zip(*route)  # Extract x and y coordinates
                        plt.plot(x, y, color=color, linewidth=2, zorder=0)

                # rest of the cables
                for house, route in routes[battery].items():
                    if house not in [self.furthest_house[battery], self.furthest_from_furthest_house[battery]]:
                        x, y = zip(*route)
                        plt.plot(x, y, color=color, linewidth=0.66, zorder=0)

            idx += 1

        # Total costs:
        total_length_cables = 0
        for battery, routes in routes.items():
            for route in routes.values():
                total_length_cables += len(route)
        
        number_of_batteries = len(connections.keys())

        cost = total_length_cables * 9 + number_of_batteries * 5000
        print(f"Total costs: {cost}")

        # Drawing details
        all_x = []
        all_y = []
        for i in range(len(self.batteries)):
            all_x.append(self.batteries[i].position[0])
        for i in range(len(self.batteries)):
            all_y.append(self.batteries[i].position[1])
        for i in range(len(self.houses)):
            all_x.append(self.houses[i].position[0])
        for i in range(len(self.houses)):
            all_y.append(self.houses[i].position[1])

        # find min and max x and y
        min_x = min(all_x)
        min_y = min(all_y)
        max_x = max(all_x)
        max_y = max(all_y)

        # Define a square based on the biggest axix
        if (max_x - min_x) > (max_y - min_y):
            # Make sure GridSize is an int
            GridSize = int(max_x - min_x)

        else:
            GridSize = int(max_y - min_y)


        xCenter = int(min_x + (max_x - min_x)/2)
        yCenter = int(min_y + (max_y - min_y)/2)

        # Plot grid lines
        for i in range(-extraGridSpace, GridSize+1 + extraGridSpace):
            # I used int()+1 so it is rounded up, int always rounds down
            plt.vlines(x = i + int(xCenter - GridSize/2)+1, ymin = int(yCenter - GridSize/2)+1-5, ymax = int(yCenter + GridSize/2)+1+5, linestyles = "-", linewidth=0.666, alpha = 0.1, zorder=-1)
            plt.hlines(y = i + int(yCenter - GridSize/2)+1, xmin = int(xCenter - GridSize/2)+1-5, xmax = int(xCenter + GridSize/2)+1+5, linestyles = "-", linewidth=0.666, alpha = 0.1, zorder=-1)
        
        # Delete labels from x and y axis
        plt.xticks([])
        plt.yticks([])
        plt.xlim(-1,GridSize+1)
        plt.ylim(-1,GridSize+1)
        plt.tight_layout()

        plt.axis('scaled')
        plt.show()


    def run(self):

        connections = self.get_connections()
        routes = self.set_cables(connections)

        # Total costs:
        total_length_cables = 0
        for battery, battery_routes in routes.items():
            for route in battery_routes.values():
                total_length_cables += len(route)

        
        number_of_batteries = len(connections.keys())

        cost = total_length_cables * 9 + number_of_batteries * 5000
        print(f"Total costs: {cost}")


        adjusted_connections = {}
        house_idx = 0
        for house_num, house in self.houses.items():
            for battery in connections.keys():
                for connected_house in connections[battery]:
                    if house == connected_house:
                        adjusted_connections[house_idx] = [house.position, battery.position]
                        house_idx += 1
                        break

        adjusted_cable_routes = {}
        cable_idx = 0
        for house_num, house in self.houses.items():
            for battery in routes.keys():
                if house in routes[battery].keys():
                    adjusted_cable_routes[cable_idx] = routes[battery][house]
                    cable_idx += 1
                    break

        return cost, adjusted_cable_routes, adjusted_connections
