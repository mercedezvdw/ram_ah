# Rembrand Ruppert, Team RAM
# Writes the data stored in our own experiment datafiles

import json

class WriteData():
    def __init__(self, districtNumber, usedAlgorithm):
        self.districtNumber = districtNumber
        self.usedAlgorithm = usedAlgorithm

    def WriteExperimentData(self, total_costs, houses, batteries, cable_routes, connections):
        """
        Writes the result of a single experiment in a .json file.
        """
        # data (testdata, real data TBD)
        data = []
        header = {"district": self.districtNumber, "costs-shared": total_costs}
        data.append(header)
        
        # create the entire dataset
        for i in range(len(batteries)):
            bat_pos_str = f"{batteries[i].position[0]},{batteries[i].position[1]}"
            houses_per_battery = []
            # if functioning correctly, len(houses) == len(cable_routes)
            for j in range(len(houses)):
                house_pos_str = f"{houses[j].position[0]},{houses[j].position[1]}"
                house_connection_pos = f"{connections[j][0][0]},{connections[j][0][1]}"
                battery_connection_pos = f"{connections[j][1][0]},{connections[j][1][1]}"
                house_output = f"{houses[j].max_output}"
                print(house_pos_str, battery_connection_pos)
                # check if the current house truly goes to this battery
                if bat_pos_str == battery_connection_pos:
                    # make a list of strings from the route
                    route = []
                    if len(cable_routes[j]):
                        for k in range(len(cable_routes[j])):
                            route_str = f"{cable_routes[j][k][0]},{cable_routes[j][k][1]}"
                            route.append(route_str)
                        
                    separate_house = {"location": house_pos_str, "output": house_output, "cables": route}
                    houses_per_battery.append(separate_house)

            battery_data = {"location": bat_pos_str, "capacity": 1507.0, "houses": houses_per_battery}
            data.append(battery_data)
        
        # serializing json
        json_object = json.dumps(data, indent=2)
        
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
  {
    "district": 1,
    "costs-shared": 10198
  },
  {
    "location": "38,12",
    "capacity": 1507.0,
    "houses": [
      {
        "location": "33,7",
        "output": 39.45690812,
        "cables": [
          "33,7",
          "33,8",
          "33,9"
        ]
      },
      {
        "location": "30,12",
        "output": 66.05341632,
        "cables": [
          "30,12",
          "31,12",
          "32,12"
        ]
      }
    ]
  },
  {
    "location": "42,3",
    "capacity": 1507.0,
    "houses": [
      {
        "location": "48,4",
        "output": 58.90934923,
        "cables": [
          "48,4",
          "48,3",
          "47,3",
          "46,3",
          "45,3",
          "44,3",
          "43,3",
          "42,3"
        ]
      }
    ]
  }
]
#'''
