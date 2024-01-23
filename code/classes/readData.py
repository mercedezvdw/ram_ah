# Rembrand Ruppert, Team RAM
# Reads the data stored in our own experiment datafiles

class ReadData():
    def __init__(self, districtNumber, usedAlgorithm):
        self.districtNumber = districtNumber
        self.usedAlgorithm = usedAlgorithm
    
    def ReadExperimentData(self):
        """
        Reads all data from the corresponding file.
        The format we use splits the data using ; instead of ',', due to the stored house, battery and cable data.
        """
        return None
    
    def ReadBestResult(self):
        """
        Returns the result with the lowest score and the corresponding map data.
        """
        return None

    def ReadWorstResult(self):
        """
        Returns the result with the highest score and the corresponding map data.
        """
        return None
