# Rembrand Ruppert, Team RAM
# Writes the data stored in our own experiment datafiles

import json

class WriteData():
    def __init__(self, districtNumber, usedAlgorithmNumber):
        self.districtNumber = districtNumber
        self.usedAlgorithmNumber = usedAlgorithmNumber

    def WriteExperimentData(self, total_costs, houses, batteries, cables):
        """
        Writes the result of a single experiment in a .json file.
        """
        # Data to be written
        dictionary = {
            "name": "sathiyajith",
            "rollno": 56,
            "cgpa": 8.6,
            "phonenumber": "9976770500"
        }
        
        # Serializing json
        json_object = json.dumps(dictionary, indent=4)
        
        # Writing to sample.json
        with open("sample.json", "w") as outfile:
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
