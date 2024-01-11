# Mercedez van der Wal & Rembrand Ruppert
# Holds the class that defines a house in our case with its properties

# import all things needed
import matplotlib.pyplot as plt
import numpy as np
from house import House
from battery import Battery
from cable import CableSegment

# function to read the supplied CSV files
def ReadCSVs(district_number):
    # create lists to store data in and a row variable to use to read file
    battery_row = 0
    house_row = 0
    batteries = {}
    houses = {}

    # read both files
    input_file_batteries = open(f'Data/district_{district_number}/district-{district_number}_batteries.csv', 'r')
    input_file_houses = open(f'Data/district_{district_number}/district-{district_number}_houses.csv', 'r')

    # go through all rows and store data into lists
    # BATTERIES
    # read
    for row_count in input_file_batteries:
        if battery_row > 0:
            row_count = row_count.strip()
            if '"' in row_count:
                row_count = row_count.replace('"','')
            data_split = row_count.split(',')
            #print(data_split)

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


def DrawCase(batteries, houses):
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
    
    # plot grid lines
    for i in range(minimum-5, maximum+6):
        plt.vlines(x = i, ymin = minimum-5, ymax = maximum+5, linestyles = "-", alpha = 0.33, zorder=-1)
        plt.hlines(y = i, xmin = minimum-5, xmax = maximum+5, linestyles = "-", alpha = 0.33, zorder=-1)
    # plot houses
    for i in range(len(houses)):
        plt.scatter(houses[i].position[0], houses[i].position[1], s = 75, color = 'r', marker = '^', label = 'house')
    # plot batteries
    for i in range(len(batteries)):
        plt.scatter(batteries[i].position[0], batteries[i].position[1], s = 75, color = 'g', marker = ',', label = 'battery')
    # plot cables
    plt.plot()
    # drawing details
    plt.xlim(-1,GridSize+1)
    plt.ylim(-1,GridSize+1)
    #plt.legend()
    plt.tight_layout()
    plt.axis('scaled')
    # actuallly plot the thing
    plt.show()

batteries, houses = ReadCSVs(0)
DrawCase(batteries, houses)
