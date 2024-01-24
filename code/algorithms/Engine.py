from code.algorithms.Rv2 import Rv2
from code.algorithms.SADDA import SADDA
from code.algorithms.NBHA import NBH_A
from code.classes.readCSV import CSVReader
from code.classes.plot import PlotCase

class Engine:

    def __init__(self, algo, district, plot) -> None:
        self.algo = algo
        self.district = district
        self.plot = plot

        file = CSVReader(f"{district}")
        self.batteries, self.houses = file.ReadCSV()


    def run(self):

        if self.algo == "Rv2":
            algo = Rv2(self.batteries, self.houses)
            cables, cable_routes = algo.run()
            
            if self.plot:
                case = PlotCase(self.batteries, self.houses, 5, cable_routes)
                case.DrawCase()

        elif self.algo == "SADDA":
            sad = SADDA(self.batteries, self.houses)
            cables, cable_routes = sad.SADDA_Run()

            if self.plot:
                case = PlotCase(self.batteries, self.houses, 5, cable_routes)
                case.DrawCase()

        elif self.algo == "NBHA":
            algo = NBH_A(self.batteries, self.houses)
            cables, cable_routes = algo.run()

            if self.plot:
                case = PlotCase(self.batteries, self.houses, 5, cable_routes)
                case.DrawCase()
        

        