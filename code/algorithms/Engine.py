# Mercedez van der Wal, Rembrand Ruppert, Yessin Radouan
# Runs all algorithms and reads/writes data

from code.algorithms.Rv2 import Rv2
from code.algorithms.SADDA import SADDA
from code.algorithms.NBHA import NBH_A
from code.algorithms.DFM import DFM
from code.classes.readCSV import CSVReader
from code.classes.plot import PlotCase
from code.classes.readData import ReadData
from code.classes.writeData import WriteData

import time

class Engine:

    def __init__(self, algo, district, plot, save_csv_data, seed) -> None:
        self.algo = algo
        self.district = district
        self.plot = plot
        self.save_csv_data = save_csv_data
        self.seed = seed

        file = CSVReader(f"{district}")
        self.batteries, self.houses = file.ReadCSV()
        self.runtime = None

    def run(self):
        RD = ReadData(self.district,self.algo)
        WD = WriteData(self.district,self.algo)
        connections = None

        t1 = time.time()


        if self.algo == "Rv2":
            algo = Rv2(self.batteries, self.houses, self.seed)
            connections, cable_routes, total_costs = algo.run()
            
            if self.plot:
                case = PlotCase(self.batteries, self.houses, 2, cable_routes, connections)
                case.DrawCase()

        elif self.algo == "SADDA":
            algo = SADDA(self.batteries, self.houses, self.seed)
            total_costs, cable_routes, connections = algo.SADDA_Run()

            if self.plot:
                case = PlotCase(self.batteries, self.houses, 2, cable_routes, connections)
                case.DrawCase()

        elif self.algo == "NBHA":
            algo = NBH_A(self.batteries, self.houses, self.seed)
            total_costs, cable_routes, connections, houses_shuffled = algo.run()
            self.houses = houses_shuffled

            if self.plot:
                case = PlotCase(self.batteries, self.houses, 2, cable_routes, connections)
                case.DrawCase()

        elif self.algo == "DFM":
            algo = DFM(self.batteries, self.houses, self.seed)
            total_costs, cable_routes, connections = algo.run()
            

            if self.plot:
                case = PlotCase(self.batteries, self.houses, 2, cable_routes, connections)
                case.DrawCase()

        t2 = time.time()
        self.runtime = t2 - t1


        ## rewriting JSON
        existing_data = RD.ReadExperimentData()

        if existing_data is not None:
            current_lowest_cost, houses_N, batteries_N, cable_routes_N, connections_N = existing_data
            if total_costs < current_lowest_cost:
                WD.WriteExperimentData(total_costs, self.houses, self.batteries, cable_routes, connections)

        else:
            WD.WriteExperimentData(total_costs, self.houses, self.batteries, cable_routes, connections)

            


        #print(self.houses) # {0: class, 1: class, ...}
        #print(self.batteries) # {0: class, 1: class, ...}
        #print(cable_routes) # {0: [[xbegin,ybegin], [xend,yend]], 1: [[xbegin,ybegin], [xend,yend]], ...}

        # WD.WriteExperimentData(total_costs, self.houses, self.batteries, cable_routes, connections)
        # total_costs_N, houses_N, batteries_N, cable_routes_N, connections_N = RD.ReadExperimentData()
        # when the house-battery assigning works correctly, these read dicts will be the same as the written ones

        # save run data to csv
        if self.save_csv_data:
            WD.WriteRunCSV(total_costs, self.runtime)

