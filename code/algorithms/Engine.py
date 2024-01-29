from code.algorithms.Rv2 import Rv2
from code.algorithms.SADDA import SADDA
from code.algorithms.NBHA import NBH_A
from code.algorithms.knn import KNN
from code.classes.readCSV import CSVReader
from code.classes.plot import PlotCase
from code.classes.readData import ReadData
from code.classes.writeData import WriteData

class Engine:

    def __init__(self, algo, district, plot) -> None:
        self.algo = algo
        self.district = district
        self.plot = plot

        file = CSVReader(f"{district}")
        self.batteries, self.houses = file.ReadCSV()

    def run(self):
        RD = ReadData(self.district,self.algo)
        WD = WriteData(self.district,self.algo)
        connections = None

        if self.algo == "Rv2":
            algo = Rv2(self.batteries, self.houses)
            total_costs, cable_routes = algo.run()
            
            if self.plot:
                case = PlotCase(self.batteries, self.houses, 5, cable_routes, connections)
                case.DrawCase()

        elif self.algo == "SADDA":
            sad = SADDA(self.batteries, self.houses)
            total_costs, cable_routes = sad.SADDA_Run()

            if self.plot:
                case = PlotCase(self.batteries, self.houses, 5, cable_routes, connections)
                case.DrawCase()

        elif self.algo == "NBHA":
            algo = NBH_A(self.batteries, self.houses)
            total_costs, cable_routes, connections = algo.run()

            if self.plot:
                case = PlotCase(self.batteries, self.houses, 5, cable_routes, connections)
                case.DrawCase()

        elif self.algo == "KNN":
            algo = KNN(self.batteries, self.houses)
            cable_routes = algo.run()

            if self.plot:
                case = PlotCase(self.batteries, self.houses, 5, cable_routes, connections)
                case.DrawCase()

        #print(self.houses) # {0: class, 1: class, ...}
        #print(self.batteries) # {0: class, 1: class, ...}
        #print(cable_routes) # {0: [[xbegin,ybegin], [xend,yend]], 1: [[xbegin,ybegin], [xend,yend]], ...}
        WD.WriteExperimentData(total_costs, self.houses, self.batteries, cable_routes)
        total_costs_N, houses_N, batteries_N, cable_routes_N = RD.ReadExperimentData()
        # when the house-battery assigning works correctly, these read dicts will be the same as the written ones
