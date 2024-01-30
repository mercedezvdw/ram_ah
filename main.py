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


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--algo", type=str,
                        help="algorithm to use: SADDA, NBHA, Rv2, DFM",
                        choices=["SADDA", "NBHA", "Rv2", "KNN", "DFM"])
    
    parser.add_argument("--district", type=str,
                        help="What district to use: test, 0, 1, 2, 3",
                        choices=["test", "0", "1", "2", "3"])
    
    parser.add_argument("--plot", action='store_true',
                    help="Plot the district. Default is False. Omit to not plot.")
    
    args = parser.parse_args()

    if args.algo not in ["SADDA", "NBHA", "Rv2", "KNN", "DFM"]:
        raise Exception("Invalid algorithm, options: SADDA, NBHA, Rv2, KNN, DFM")
    
    if args.district not in ["test", "0", "1", "2", "3"]:
        raise Exception("Invalid district, options: test, 0, 1, 2, 3")
    
    
    engine = Engine(args.algo, args.district, args.plot)
    engine.run()
    
    






