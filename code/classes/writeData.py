# Rembrand Ruppert, Team RAM
# Writes the data stored in our own experiment datafiles

class WriteData():
    def __init__(self, districtNumber, usedAlgorithm):
        self.districtNumber = districtNumber
        self.usedAlgorithm = usedAlgorithm

    def WriteExperimentData(self):
        """
        Writes the result of a single experiment in a csv file.
        The format we use splits the data using ; instead of ',', due to the stored house, battery and cable data.
        """
        return None
    
    def ClearExperimentData(self):
        """
        Clears all data from a file for a hard reset, when significant changes are made.
        """
        return None
