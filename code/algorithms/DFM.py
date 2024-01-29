# Yessin Radouane, Team RAM
# Depth First Mycelium Algorithm (DFM) (Finds furthest house from battery and the house furthest from that house, connects them with a cable, then connects the rest of the houses to the closest cable or battery)

import math
from matplotlib import pyplot as plt

class DFM():

    def __init__(self, batteries, houses):
        
        self.batteries = batteries
        self.houses = houses
        self.furthest_house = {}
        self.furthest_from_furthest_house = {}

    def calculate_distance(self, c1, c2):
        """
        Calculate the distance between two coordinates
        """
        distance = math.sqrt(((c1[0] - c2[0]) ** 2) + ((c1[1] - c2[1]) ** 2))
        return distance
    
    def get_connections(self):
        connections = {}
        distances = {}
        connected_houses = set(self.houses.keys())

        # Calculate distance from house to each battery and sort batteries by distance for each house
        for house_num, house in self.houses.items():
            distances[house] = sorted(
                self.batteries.items(),
                key=lambda item: self.calculate_distance(house.position, item[1].position)
            )

        # Group houses per battery based on distance, account for capacity
        for house_num, house in self.houses.items():
            for battery_num, battery in distances[house]:
                if battery.capacity >= house.max_output:
                    if battery not in connections:
                        connections[battery] = []
                    connections[battery].append(house)
                    battery.capacity -= house.max_output
                    connected_houses.remove(house_num)
                    break

        # Attempt to connect unconnected houses
        for house_num in list(connected_houses):
            house = self.houses[house_num]
            for battery_num, battery in distances[house]:
                for connected_house in connections.get(battery, []):
                    # Check if switching is possible
                    second_closest_battery = next((b for b_num, b in distances[connected_house] if b != battery and b.capacity + connected_house.max_output >= house.max_output), None)
                    if second_closest_battery:
                        # Switch the connection
                        connections[battery].remove(connected_house)
                        battery.capacity += connected_house.max_output

                        if second_closest_battery not in connections:
                            connections[second_closest_battery] = []
                        connections[second_closest_battery].append(connected_house)
                        second_closest_battery.capacity -= connected_house.max_output

                        # Connect the unconnected house
                        connections[battery].append(house)
                        battery.capacity -= house.max_output
                        connected_houses.remove(house_num)
                        break
                if house_num not in connected_houses:
                    break

        # Check if any houses are still left unconnected
        if len(connected_houses) > 0:
            print("Houses that couldn't be connected:", connected_houses)

        return connections
    

    def check_best_move(self, current_position, end_position, illegal_move = None):
        """ This function checks which move minimizes the distance to the end position and returns that move.
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

        best_move = None

        # remove the move that adds the most distance to the end position
        if distance_1 == min(distances):
            best_move = move_1
            
        elif distance_2 == min(distances):
            best_move = move_2

        elif distance_3 == min(distances):
            best_move = move_3

        # print(best_move)
        return best_move
    

        
    def generate_routes(self, start_position, end_position):
        """
        Greedy walk generates the route per connection
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
            # print(new_position)

            # Make sure it's within the grid size
            if 0 <= new_position[0] <= 50 and 0 <= new_position[1] <= 50:
                current_position = new_position
                route.append(current_position)

        # print(route)
        return route
        

    def set_cables(self, connections):

        routes = {}

        furthest_house = None
        longest_distance = 0
        furthest_from_furthest_house = None
        second_distance = 0
                
    
        # Creaste base cables for furthest house and furthest house from this house
        for battery in connections.keys():
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
            
    
        # print(routes)

        # now to connect the rest of the houses per battery
        # go depth first, so find the furthes house and connect to closest cable or linked battery

        for battery in connections.keys():
            unconnected_houses = [house for house in connections[battery] if house not in [self.furthest_house[battery], self.furthest_from_furthest_house[battery]]]
               
            # find furthest house from battery and make routes until all houses are connected
            # print(f"STARTING WITH {len(unconnected_houses)} unconnected houses")
            while len(unconnected_houses) > 0:
                furthest_house = None
                longest_distance = 0
                for house in unconnected_houses:
                    distance = self.calculate_distance(battery.position, house.position)
                    if distance > longest_distance:
                        longest_distance = distance
                        furthest_house = house
    
                # find closest cable or linked battery
                smallest_distance_cable = 1e9
                distance_battery = None
                closest_cable = None
                for route in routes[battery].values():

                    #find closest cable
                    for cable in route:
                        distance = self.calculate_distance(cable, furthest_house.position)
                        if distance < smallest_distance_cable:
                            smallest_distance_cable = distance
                            closest_cable = cable

                # find closest battery
                distance_battery = self.calculate_distance(battery.position, furthest_house.position)

                if distance_battery < smallest_distance_cable:
                    # connect to battery
                    route = self.generate_routes(battery.position, furthest_house.position)

                    # add route to routes
                    routes[battery][furthest_house] = route


                    # remove house from unconnected houses
                    unconnected_houses.remove(furthest_house)

                else:
                    # connect to closest cable
                    route = self.generate_routes(closest_cable, furthest_house.position)

                    # add route to routes
                    routes[battery][furthest_house] = route

                    # remove house from unconnected houses
                    unconnected_houses.remove(furthest_house)
                        
        # print(f"PRINTING FROM ROUTES FUNCTION: {routes}")
        return routes


    


        

            
    
    def DrawCase(self, connections, routes, extraGridSpace = 5):
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

        # total costs:
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

        # define a square based on the biggest axix
        if (max_x - min_x) > (max_y - min_y):
            # make sure GridSize is an int
            GridSize = int(max_x - min_x)
            minimum = min_x
            maximum = max_x
        else:
            GridSize = int(max_y - min_y)
            minimum = min_y
            maximum = max_y

        xCenter = int(min_x + (max_x - min_x)/2)
        yCenter = int(min_y + (max_y - min_y)/2)

        # plot density map
        #cmap = plt.set_cmap('inferno')
        #plt.scatter(DensityMap[:, 0:1], DensityMap[:, 1:2], c=DensityMap[:, 2:3], cmap=cmap, marker=',', s=55, alpha=1, zorder=-2)
        #plt.colorbar()

        # plot grid lines
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


        # total costs:
        total_length_cables = 0
        for battery, battery_routes in routes.items():
            for route in battery_routes.values():
                total_length_cables += len(route)

        
        number_of_batteries = len(connections.keys())

        cost = total_length_cables * 9 + number_of_batteries * 5000
        print(f"Total costs: {cost}")

        adjusted_connections = {}
        adjusted_routes = {}
        house_num = 0

        for battery, houses in connections.items():
            # print(battery, houses)
            # print()
            for house in houses:
                adjusted_connections[house_num] = [house.position, battery.position]
                adjusted_routes[house_num] = routes[battery][house]

                house_num += 1

       
        return cost, routes, connections