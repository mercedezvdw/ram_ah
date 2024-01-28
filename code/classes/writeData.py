# Rembrand Ruppert, Team RAM
# Writes the data stored in our own experiment datafiles

import json

class WriteData():
    def __init__(self, districtNumber, usedAlgorithm):
        self.districtNumber = districtNumber
        self.usedAlgorithm = usedAlgorithm

    def WriteExperimentData(self, total_costs, houses, batteries, cable_routes):
        """
        Writes the result of a single experiment in a .json file.
        """
        # data (testdata, real data TBD)
        data = []
        header = {"district": self.districtNumber, "costs-shared": total_costs}
        data.append(header)
        
        # create the entire dataset
        for i in range(len(batteries)):
            houses_pathing = []
            for j in range(len(houses)):
                houses_pathing.append(cable_routes)
            bat_pos_str = f"{batteries[i].position[0]},{batteries[i].position[1]}"
            battery_data = {"location": bat_pos_str, "capacity": 1507.0, "houses": houses_pathing}
            data.append(battery_data)
        
        # serializing json
        json_object = json.dumps(data, indent=4)
        
        # writing to file
        with open(f"data/results/district_{self.districtNumber}/district-{self.districtNumber}_{self.usedAlgorithm}.json", "w") as outfile:
            outfile.write(json_object)

        return None

    
    def ClearExperimentData(self):
        """
        Clears all data from a file for a hard reset, when significant changes are made.
        """
        return None
    

# JSON FORMAT:
'''
[
  {"district": 1, "costs-shared": 10198},
  {"location": "38,12", "capacity": 1507.0, "houses": [
      {
        "location": "33,7",
        "output": 39.45690812,
        "cables": ["33,7", "33,8", "33,9", "33,10", "33,11", "33,12", "34,12", "35,12", "36,12", "37,12", "38,12"]
      },
      {
        "location": "30,12",
        "output": 66.05341632,
        "cables": ["30,12", "31,12", "32,12", "33,12", "34,12"]
      }]
  },
  {"location": "42,3", "capacity": 1507.0, "houses": [
      {
        "location": "48,4",
        "output": 58.90934923,
        "cables": ["48,4", "48,3", "47,3", "46,3", "45,3", "44,3", "43,3", "42,3"]
      }]
  }
]
#'''
