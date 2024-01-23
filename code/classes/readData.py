# Rembrand Ruppert, Team RAM
# Reads the data stored in our own experiment datafiles

from code.classes.house import House
from code.classes.battery import Battery
from code.classes.cable import CableSegment

class ReadData():
    def __init__(self, districtNumber, usedAlgorithmNumber):
        self.districtNumber = districtNumber
        self.usedAlgorithmNumber = usedAlgorithmNumber
    
    def ReadExperimentData(self):
        """
        Reads all data from the corresponding file.
        The format we use splits the data using ; instead of ',', due to the stored house, battery and cable data.
        format:
        total_costs (int value); houses ([x,y,maxoutput]); batteries ([x,y,capacity]); cables ([x_beign,y_begin,x_end,y_end])
        """
        # create lists to store data in and a row variable to use to read file
        row = 0
        file_total_costs = []
        file_batteries = []
        file_houses = []
        file_cables = []

        # read both files
        input_file = open(f'data/results/district-{self.districtNumber}_alg{self.usedAlgorithmNumber}.csv', 'r')

        # go through all rows and store data into lists
        # BATTERIES
        # read
        for row_count in input_file:
            total_costs = {}
            batteries = {}
            houses = {}
            cables = {}

            if row > 0:
                row_count = row_count.strip()
                if '"' in row_count:
                    row_count = row_count.replace('"','')
                data_split = row_count.split(';')
                
                # now that the data is split by ';', we can store all separate data formats
                '''
                # store data
                total_costs[row-1] = int(data_split[0])
                # houses
                data_split[1].split(',')
                houses[row-1] = House([int(data_split[0]), int(data_split[1])], float(data_split[2]))
                # batteries
                data_split[2].split(',')
                batteries[row-1] = Battery([int(data_split[0]), int(data_split[1])], float(data_split[2]))
                # cables
                data_split[3].split(',')
                cables[row-1] = CableSegment([int(data_split[0]), int(data_split[1])], float(data_split[2]))
                #'''

            row += 1

        input_file.close()

        return file_total_costs, file_batteries, file_houses, file_cables

    
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
