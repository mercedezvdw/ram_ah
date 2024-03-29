# Rembrand Ruppert, Team RAM
# Writes the data stored in our own experiment datafiles

import json
import os
import csv

class WriteData():
    def __init__(self, districtNumber, usedAlgorithm):
        self.districtNumber = districtNumber
        self.usedAlgorithm = usedAlgorithm

    def WriteExperimentData(self, total_costs, houses, batteries, cable_routes, connections):
        """
        Writes the result of a single experiment in a .json file.
        """
        # Data (testdata, real data TBD)
        data = []
        header = {"district": self.districtNumber, "costs-shared": total_costs}
        data.append(header)
        
        # Create the entire dataset
        for i in range(len(batteries)):
            bat_pos_str = f"{batteries[i].position[0]},{batteries[i].position[1]}"
            houses_per_battery = []

            # If functioning correctly, len(houses) == len(cable_routes)
            for j in range(len(houses)):
                house_pos_str = f"{houses[j].position[0]},{houses[j].position[1]}"
                house_connection_pos = f"{connections[j][0][0]},{connections[j][0][1]}"
                battery_connection_pos = f"{connections[j][1][0]},{connections[j][1][1]}"
                house_output = f"{houses[j].max_output}"

                # Check if the current house truly goes to this battery
                if bat_pos_str == battery_connection_pos:

                    # Make a list of strings from the route
                    route = []
                    if cable_routes.get(j) is not None and len(cable_routes[j]):
                        for k in range(len(cable_routes[j])):
                            route_str = f"{cable_routes[j][k][0]},{cable_routes[j][k][1]}"
                            route.append(route_str)

                    separate_house = {"location": house_pos_str, "output": house_output, "cables": route}
                    houses_per_battery.append(separate_house)

            battery_data = {"location": bat_pos_str, "capacity": 1507.0, "houses": houses_per_battery}
            data.append(battery_data)

        # Serializing json
        json_object = json.dumps(data, indent=2)

        # Writing to file
        with open(f"data/results/district_{self.districtNumber}/district-{self.districtNumber}_{self.usedAlgorithm}.json", "w") as outfile:
            outfile.write(json_object)

        return None

    
    def ClearExperimentData(self):
        """
        Clears all data from a file for a hard reset, when significant changes are made.
        """
        return None
    
    def WriteRunCSV(self, total_costs, run_time):
        """
        Writes the results of a run in a .csv file.
        """
        file_name = f"data/algo_scores/{self.usedAlgorithm}.csv"  # Name of the CSV file
        file_exists = os.path.isfile(file_name)  # Check if file already exists

        with open(file_name, mode='a', newline='') as file:  # Open the file in append mode
            writer = csv.writer(file)

            if not file_exists:
                # Write the header if the file doesn't exist
                writer.writerow(['Run ID', 'District Number', 'Total Costs', 'Run Time'])

            # Determine the next index
            if file_exists:
                
                # If file exists, find the last index
                with open(file_name, mode='r') as read_file:
                    last_line = list(csv.reader(read_file))[-1]
                    last_index = int(last_line[0])
                    next_index = last_index + 1
            else:
                next_index = 1  # Start from 1 if file doesn't exist

            # Write the new data
            writer.writerow([next_index, self.districtNumber, total_costs, run_time])
            

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
