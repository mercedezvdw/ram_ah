# Rembrand Ruppert
# Density Computing Algorithm (DCA) (uses either KNN or altered SPH density calculations / compute house density and create subdistricts)
# Use grid node system to find density across nodes.

import numpy as np

class DensityComputation():
    def __init__(self, BatteryList, HouseList):
        self.BatteryPosList = BatteryList
        self.HousePosList = HouseList
        