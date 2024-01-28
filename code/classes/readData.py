# Rembrand Ruppert, Team RAM
# Reads the data stored in our own experiment datafiles

from code.classes.house import House
from code.classes.battery import Battery
from code.classes.cable import CableSegment
import json

class ReadData():
    def __init__(self, districtNumber, usedAlgorithmNumber):
        self.districtNumber = districtNumber
        self.usedAlgorithmNumber = usedAlgorithmNumber
    
    def ReadExperimentData(self):
        """
        Reads all data from the corresponding file.
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
