# Rembrand Ruppert, Team RAM
# Writes the data stored in our own experiment datafiles

class WriteData():
    def __init__(self, districtNumber, usedAlgorithmNumber):
        self.districtNumber = districtNumber
        self.usedAlgorithmNumber = usedAlgorithmNumber

    def WriteExperimentData(self, total_costs, houses, batteries, cables):
        """
        Writes the result of a single experiment in a .json file.
        """
        return None

    
    def ClearExperimentData(self):
        """
        Clears all data from a file for a hard reset, when significant changes are made.
        """
        return None