# Rembrand Ruppert, Team RAM
# Reads the data stored in our own experiment datafiles

from code.classes.house import House
from code.classes.battery import Battery
from code.classes.cable import CableSegment
import json

class ReadData():
    def __init__(self, districtNumber, usedAlgorithm):
        self.districtNumber = districtNumber
        self.usedAlgorithm = usedAlgorithm
    
    def ReadExperimentData(self):
        """
        Reads all data from the corresponding file.
        """
        # open file
        file = open(f"data/results/district_{self.districtNumber}/district-{self.districtNumber}_{self.usedAlgorithm}.json")
        
        # returns JSON object as 
        # a dictionary
        data = json.load(file)
        
        # Iterating through the json
        # list
        for i in data:
            print(i, "\n")
        
        # Closing file
        file.close()
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
