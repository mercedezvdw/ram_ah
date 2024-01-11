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
    battery_position = []
    battery_capacity = []
    house_position = []
    house_maxoutput = []

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
            battery_position.append([data_split[0], data_split[1]])
            battery_capacity.append(data_split[2])
        battery_row += 1

    input_file_batteries.close()

    # HOUSES
    for row_count in input_file_houses:
        if house_row > 0:
            row_count = row_count.strip()
            data_split = row_count.split(',')
            print(data_split)
            house_position.append([data_split[0], data_split[1]])
            house_maxoutput.append(data_split[2])
        house_row += 1

    input_file_houses.close()

    return battery_position, battery_capacity, house_position, house_maxoutput


def DrawCase(GridSize):
    # plot grid lines
    for i in range(GridSize+1):
        plt.vlines(x = i, ymin = 0, ymax = GridSize, linestyles = ":", alpha = 0.5)
        plt.hlines(y = i, xmin = 0, xmax = GridSize, linestyles = ":", alpha = 0.5)
    # plot houses
    plt.plot()
    # plot batteries
    plt.plot()
    # plot cables
    plt.plot()
    # drawing details
    plt.xlim(-1,GridSize+1)
    plt.ylim(-1,GridSize+1)
    plt.legend()
    plt.tight_layout()
    plt.axis('scaled')
    # actuallly plot the thing
    plt.show()

ReadCSVs(1)
DrawCase(10)