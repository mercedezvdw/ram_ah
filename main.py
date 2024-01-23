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
from code.classes.plot import PlotCase
from code.classes.readCSV import CSVReader
from code.algorithms.SADDA import SADDA
from code.algorithms.NBHA import NBH_A
from code.classes.readData import ReadData
from code.classes.writeData import WriteData


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


if __name__ == "__main__":
    # do something with command line inputs
    # for example:
    # > python main.py 1 SADDA 1000
    # [0]: district number
    # [1]: what algorithm to use and where to store it (1 file per algorithm per district)
    # [2]: number of runs
    # [3]: TBD




    # read the file and save battery and house positions
    district = "0"
    file = CSVReader(f"{district}")
    batteries, houses = file.ReadCSV()

    # alg 1 - SADDA
    sad = SADDA(batteries, houses)
    posses = sad.GetPosList()
    centroids = sad.GetCentroidPositions(posses)
    HBC = sad.GetHouseBatteryConnection(posses, centroids)
    #print(HBC)

    # alg 2
    connections = make_connections(houses, batteries)
    # print(connections)
    MW_Alg = NBH_A(batteries, houses)
    cables, cable_routes = MW_Alg.NBH_Algorithm()

    # draw
    case = PlotCase(batteries, houses, cables, 5, connections, cable_routes, centroids)
    case.DrawCase()





