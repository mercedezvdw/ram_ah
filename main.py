# Mercedez van der Wal, Rembrand Ruppert, Yessin Radouan
# Holds the class that defines a house in our case with its properties

# import all things needed
import matplotlib.pyplot as plt
import numpy as np
import random
from code.classes.house import House
from code.classes.battery import Battery
from code.classes.cable import CableSegment
from code.algorithms.DCA import DensityComputation
from code.algorithms.randomise import *
from code.algorithms.NBHA import *


# function to read the supplied CSV files
def ReadCSVs(district_number):
    """
    Reads the supplied .csv-files and stores the data in objects.
    """
    # create lists to store data in and a row variable to use to read file
    battery_row = 0
    house_row = 0
    batteries = {}
    houses = {}

    # read both files
    input_file_batteries = open(f'data/district_{district_number}/district-{district_number}_batteries.csv', 'r')
    input_file_houses = open(f'data/district_{district_number}/district-{district_number}_houses.csv', 'r')

    # go through all rows and store data into lists
    # BATTERIES
    # read
    for row_count in input_file_batteries:
        if battery_row > 0:
            row_count = row_count.strip()
            if '"' in row_count:
                row_count = row_count.replace('"','')
            data_split = row_count.split(',')
            # print(data_split)

            # store data
            batteries[battery_row-1] = Battery([int(data_split[0]), int(data_split[1])], float(data_split[2]))
        battery_row += 1

    input_file_batteries.close()

    # HOUSES
    for row_count in input_file_houses:
        if house_row > 0:
            row_count = row_count.strip()
            data_split = row_count.split(',')
            #print(data_split)
            houses[house_row-1] = House([int(data_split[0]), int(data_split[1])], float(data_split[2]))
        house_row += 1

    input_file_houses.close()

    #print(batteries[0].position)
    #print(houses[0].position)

    return batteries, houses

def ConnectCables_repo():
    """
    Connects cables from houses to batteries
    """
    # ---------------------- REPRESENTATION ONLY ----------------------
    # this part is hard coded for now, create and use algorithms for baseline and on
    #29,36 - b
    #34,47 - h1 - cable 11 down and 5 left
    #24,22 - h2 - cable 14 up and 5 right
    cables = {}
    # for now do all steps in one direction in a loop
    pos_battery = batteries[0].position
    pos_house_1 = houses[0].position
    pos_house_2 = houses[1].position
    cable_price = 10

    pos_begin = pos_house_1
    # left
    for i in range(0,abs(batteries[0].position[0] - houses[0].position[0])):
        if i > 0:
            pos_begin = pos_end
        pos_end = np.subtract(pos_begin, [1,0])
        #print(pos_begin, pos_end)
        cables[i] = CableSegment(pos_begin, pos_end, cable_price)
    j = abs(batteries[0].position[0] - houses[0].position[0])
    # down
    for i in range(j, j + abs(batteries[0].position[1] - houses[0].position[1])):
        if i > 0:
            pos_begin = pos_end
        pos_end = np.subtract(pos_begin, [0,1])
        #print(pos_begin, pos_end)
        cables[i] = CableSegment(pos_begin, pos_end, cable_price)
    j += abs(batteries[0].position[1] - houses[0].position[1])

    pos_begin = pos_house_2
    # right
    for i in range(j,j+abs(batteries[0].position[0] - houses[1].position[0])):
        if i > j:
            pos_begin = pos_end
        pos_end = np.subtract(pos_begin, [-1,0])
        #print(pos_begin, pos_end)
        cables[i] = CableSegment(pos_begin, pos_end, cable_price)
    j += abs(batteries[0].position[0] - houses[1].position[0])
    # up
    for i in range(j, j + abs(batteries[0].position[1] - houses[1].position[1])):
        if i > 0:
            pos_begin = pos_end
        pos_end = np.subtract(pos_begin, [0,-1])
        #print(pos_begin, pos_end)
        cables[i] = CableSegment(pos_begin, pos_end, cable_price)
    j += abs(batteries[0].position[1] - houses[1].position[1])

    return cables

    # ---------------------- RANDOM WALK ALGORITHM ----------------------
def ConnectCables():
    """
    Connects cables from houses to batteries
    """
    cable_price = 10
    cables = {}
    i = 0
    
    for house, battery in connections.items():
            pos_begin = house.position
            pos_end = battery.position
        
            cables[i] = CableSegment(pos_begin, pos_end, cable_price)
            i += 1

    return cables
    
# ------------------- NEAREST BATTERY HEURISTIC ALGORITHM -------------------
def NBH_Algorithm():
    """
    Execute Nearest Battery Heuristic Algorithm
    """
    cables = {}
    cable_routes = {}
    sum_costs = 5000 * (len(batteries))
    assign_again = []
    
    
    houses_items = list(houses.items())
    houses_items.sort(key=lambda item: item[1].max_output)
    sorted_houses = dict(houses_items)
    
    houses_copy = houses.copy()
    # # Random choice of order to assign each house to a cable
    # shuffled_indexes = list(range(len(houses)))
    # random.shuffle(shuffled_indexes)
    # print(shuffled_indexes)
    
    for i in range(len(houses_copy)):
        # Check if there is already a cable path through this house
        path = find_cable_path(houses_copy[i].position, cable_routes, batteries, houses_copy[i].max_output)
        if path is not None:
            connection = path.position
            closest_option = None
            route_costs = 0

        else:
            # Find closest battery with sufficient capacity
            closest_battery = find_closest_battery(houses_copy[i], batteries, cable_routes, cables, assign_again)

            # Find the closest cable and which battery it is connected to
            closest_cable, connected_battery = find_closest_cable(cable_routes, houses_copy[i].position, houses_copy[i].max_output, batteries, cables)

            # If there is no cable to connect to, there comes a new cable to the closest battery
            if closest_cable is None:
                closest_option = closest_battery.position
                connection = closest_battery.position
                cable_route = create_cable_route(houses_copy[i].position, closest_battery.position, houses_copy, closest_battery)

            # Compare the closest cable and the closest battery to decide which option is more close
            else:
                closest_option = compare_results(houses_copy[i].position, closest_battery.position, closest_cable)

                # If the battery itself is closer, the cable will be connected to the closest battery
                if closest_option == closest_battery.position:
                    connection = closest_battery.position
                    cable_route = create_cable_route(houses_copy[i].position, closest_battery.position, houses_copy, closest_battery)

                # If not, the connected battery is from the closest cable
                else:
                    cable_route = create_cable_route(houses_copy[i].position, closest_option, houses_copy, connected_battery)
                    connection = connected_battery.position
            
            route_costs = (len(cable_route) - 1) * 9
            cable_routes[i] = cable_route

        print(f"For house {houses[i].position} the closest option is {closest_option}, battery = {connection}")
        
        # Add houses from 'assign again' to the for loop
        for j in range(len(assign_again)):
            houses_copy[i + j] = assign_again[j - 1]
            del assign_again[j - 1]
            j += 1
        
        cables[i] = CableSegment(houses_copy[i].position, connection, route_costs)
        sum_costs += route_costs

        # print(f"begin: {cables[i].pos_begin}, end: {cables[i].pos_end}")

        battery = find_battery(batteries, connection)
        battery.add_used_capacity(houses_copy[i].max_output)
    
    if assign_again == []:
        print(f"The total price of the cables is {sum_costs}")
        return cables, cable_routes

def DrawCase(batteries, houses, cables, extraGridSpace, connections, cable_routes):
    """
    Draws a map of the chosen district showing all houses, battries and cables

    NOTE: cables argument is not used!
    """
    # create a merged list of all positions and get the minimum and maximum x and y values to make a map
    # add all x and y to respective lists
    all_x = []
    all_y = []
    for i in range(len(batteries)):
        all_x.append(batteries[i].position[0])
    for i in range(len(batteries)):
        all_y.append(batteries[i].position[1])
    for i in range(len(houses)):
        all_x.append(houses[i].position[0])
    for i in range(len(houses)):
        all_y.append(houses[i].position[1])

    # find min and max x and y
    min_x = min(all_x)
    min_y = min(all_y)
    max_x = max(all_x)
    max_y = max(all_y)
    #print(all_x, all_y)
    #print(min_x, min_y, max_x, max_y)

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

    # plot grid lines
    for i in range(-extraGridSpace, GridSize+1 +extraGridSpace):
        # I used int()+1 so it is rounded up, int always rounds down
        plt.vlines(x = i + int(xCenter - GridSize/2)+1, ymin = int(yCenter - GridSize/2)+1-5, ymax = int(yCenter + GridSize/2)+1+5, linestyles = "-", alpha = 0.33, zorder=-1)
        plt.hlines(y = i + int(yCenter - GridSize/2)+1, xmin = int(xCenter - GridSize/2)+1-5, xmax = int(xCenter + GridSize/2)+1+5, linestyles = "-", alpha = 0.33, zorder=-1)
    # plot houses
    for i in range(len(houses)):
        plt.scatter(houses[i].position[0], houses[i].position[1], s = 75, color = 'r', marker = '^', label = 'house', zorder=1)
    # plot batteries
    for i in range(len(batteries)):
        plt.scatter(batteries[i].position[0], batteries[i].position[1], s = 75, color = 'g', marker = ',', label = 'battery', zorder=1)
    # plot cables
    #for i in range(len(cables)):
    #    plt.plot([cables[i].pos_begin[0], cables[i].pos_end[0]], [cables[i].pos_begin[1], cables[i].pos_end[1]], color='b', zorder=0)

    # ---------------------- RANDOM WALK ALGORITHM ----------------------
    # route_lengths = []
    #
    # for house, battery in connections.items():
    #
    #     route = generate_routes(house.position, battery.position)
    #     route_lengths.append({"from": house, "to": battery, "length": len(route)})
    #
    #     # print(route)
    #     print(f"Route from House at {house.position} to Battery {battery.position} is {len(route)} steps long.\n")
    #     # Plot cable route
    #     x, y = zip(*route)
    #     plt.plot(x, y, color='b', zorder=0)
    #
    # total_length = sum([route["length"] for route in route_lengths])
    # print(f"Total length of all routes is {total_length}.\n")
    
    # ------------------- NEAREST BATTERY HEURISTIC ALGORITHM -------------------
    # Plot cables
    for key, route in cable_routes.items():
        x, y = zip(*route)
        plt.plot(x, y, color='b', zorder=0)
    
    # drawing details
    plt.xlim(-1,GridSize+1)
    plt.ylim(-1,GridSize+1)
    #plt.legend()
    
    plt.tight_layout()
    plt.axis('scaled')
    # actuallly plot the thing
    plt.show()

batteries, houses = ReadCSVs(1)
connections = make_connections(houses, batteries)
# print(connections)
cables, cable_routes = NBH_Algorithm()
DrawCase(batteries, houses, cables, 5, connections, cable_routes)
