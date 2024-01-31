# Mercedez van der Wal, Rembrand Ruppert, Yessin Radouan
# Distributes the input values to create a certain set of algorithm runs

# import all things needed
import matplotlib.pyplot as plt
import numpy as np
import random
from code.classes.house import House
from code.classes.battery import Battery
from code.classes.cable import CableSegment
from code.classes.plot import PlotCase
from code.classes.readCSV import CSVReader
from code.algorithms.SADDA import SADDA
from code.algorithms.NBHA import NBH_A
from code.classes.readData import ReadData
from code.classes.writeData import WriteData

from code.algorithms.Rv2 import Rv2
from code.algorithms.Engine import Engine
import argparse

if __name__ == "__main__":
    seed = 42
    np.random.seed(seed)

    parser = argparse.ArgumentParser()

    parser.add_argument("--algo", type=str,
                        help="algorithm to use: SADDA, NBHA, Rv2, DFM",
                        choices=["SADDA", "NBHA", "Rv2", "KNN", "DFM"])
    
    parser.add_argument("--district", type=str,
                        help="What district to use: test, 0, 1, 2, 3",
                        choices=["test", "0", "1", "2", "3"])
    
    parser.add_argument("--plot", action='store_true',
                    help="Plot the district. Default is False. Omit to not plot.")
    
    parser.add_argument("--save_csv", action='store_true',
                    help="Save the data from this run to a csv file. Default is False. Omit to not save.")
    
    parser.add_argument("--mass_run", type=int,
                    help="Use this to run the algorithm multiple times. Default is 1.")
    
    args = parser.parse_args()

    if args.algo not in ["SADDA", "NBHA", "Rv2", "KNN", "DFM"]:
        raise Exception("Invalid algorithm, options: SADDA, NBHA, Rv2, KNN, DFM")
    
    if args.district not in ["test", "0", "1", "2", "3"]:
        raise Exception("Invalid district, options: test, 0, 1, 2, 3")
    
    if args.mass_run is None:
        args.mass_run = 1
    
    for i in range(args.mass_run):
        engine = Engine(args.algo, args.district, args.plot, args.save_csv, seed)
        engine.run()
        seed += 1
