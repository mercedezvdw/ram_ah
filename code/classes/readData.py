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
        houses = {}
        batteries = {}
        cable_routes = {}
        
        # Open file
        file = open(f"data/results/district_{self.districtNumber}/district-{self.districtNumber}_{self.usedAlgorithm}.json")
        
        # Returns JSON object as dictionary
        try: 
            data = json.load(file)
        except:
            print("Error: File not found")
            return None
        
        bat_nr = 0
        house_nr = 0
        
        # Go through each line
        for i in data:
            if list(i.keys())[1] == "costs-shared":
                total_costs = int(list(i.values())[1])

            for j in range(len(i)):
                
                # Register batteries
                if list(i.keys())[j] == "location":
                    coords = (list(i.values())[j]).split(',')
                    capacity = list(i.values())[j+1]
                    batteries[bat_nr] = Battery([int(coords[0]), int(coords[1])], float(capacity))      # pos + capacity
                    bat_nr += 1
                    
                # Register houses
                if list(i.keys())[j] == "houses":
                    
                    # Go through each house registered under a single battery
                    for k in range(len(list(i.values())[j])):
                        cable_coords = []
                        
                        # Convert all cable route coords to ints and put each route into its own dict kay value pair
                        for L in range(0,len(list(i.values())[j][k]['cables'])):
                            cable_coord = [int((list(i.values())[j][k]['cables'][L]).split(',')[0]), int((list(i.values())[j][k]['cables'][L]).split(',')[1])]
                            cable_coords.append(cable_coord)
                            
                        # Add to a dict
                        cable_routes[house_nr] = cable_coords

                        coords = (list(i.values())[j][k]['location']).split(',')
                        houses[house_nr] = House([int(coords[0]), int(coords[1])], (list(i.values())[j]))          # pos + output
                        house_nr += 1
        
        file.close()
        connections = None

        return total_costs, houses, batteries, cable_routes, connections

    
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
