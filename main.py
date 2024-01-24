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

from code.algorithms.Rv2 import *
from code.algorithms.Engine import Engine
import argparse


#     # ---------------------- RANDOM WALK ALGORITHM ----------------------
# def ConnectCables():
#     """
#     Connects cables from houses to batteries
#     """
#     cable_price = 10
#     cables = {}
#     i = 0
    
#     for house, battery in connections.items():
#             pos_begin = house.position
#             pos_end = battery.position
        
#             cables[i] = CableSegment(pos_begin, pos_end, cable_price)
#             i += 1

#     return cables


if __name__ == "__main__":
    # do something with command line inputs
    # for example:
    # > python main.py 1 SADDA 1000
    # [0]: district number
    # [1]: what algorithm to use and where to store it (1 file per algorithm per district)
    # [2]: number of runs
    # [3]: TBD




    # read the file and save battery and house positions
    # district = "1"
    # file = CSVReader(f"{district}")
    # batteries, houses = file.ReadCSV()

    # # alg 1 - SADDA
    
    # sad = SADDA(batteries, houses)
    # cables, cable_routes = sad.SADDA_Run()

    

    # alg 2
    '''
    connections = make_connections(houses, batteries)
    #print(connections)
    MW_Alg = NBH_A(batteries, houses)
    cables, cable_routes = MW_Alg.NBH_Algorithm()
    #'''

    # alg 3
    #...

    # alg 4 Random v2

    # algo = Randomise_v2(batteries, houses)
    # cables, cable_routes = algo.run()


    # alg 5 NBHA
    # algo = NBH_A(batteries, houses)
    # cables, cable_routes = algo.run()

    # alg 6 Random



    # draw
    # case = PlotCase(batteries, houses, 5, cable_routes)
    # case.DrawCase()


    
    parser = argparse.ArgumentParser()

    parser.add_argument("--algo", type=str,
                        help="algorithm to use: SADDA, NBHA, Rv2",
                        choices=["SADDA", "NBHA", "Rv2"])
    
    parser.add_argument("--district", type=str,
                        help="What district to use: test, 0, 1, 2, 3",
                        choices=["test", "0", "1", "2", "3"])
    
    parser.add_argument("--plot", action='store_true',
                    help="Plot the district. Default is False. Omit to not plot.")
    
    args = parser.parse_args()

    if args.algo not in ["SADDA", "NBHA", "Rv2"]:
        raise Exception("Invalid algorithm, options: SADDA, NBHA, Rv2")
    
    if args.district not in ["test", "0", "1", "2", "3"]:
        raise Exception("Invalid district, options: test, 0, 1, 2, 3")
    
    
    engine = Engine(args.algo, args.district, args.plot)
    engine.run()
    
    

    # engine = Engine(args.algo, district, True)





