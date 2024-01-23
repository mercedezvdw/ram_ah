# Rembrand Ruppert, Team RAM
# Writes the data stored in our own experiment datafiles

class WriteData():
    def __init__(self, districtNumber, usedAlgorithmNumber):
        self.districtNumber = districtNumber
        self.usedAlgorithmNumber = usedAlgorithmNumber

    def WriteExperimentData(self, total_costs, houses, batteries, cables):
        """
        Writes the result of a single experiment in a csv file.
        The format we use splits the data using ; instead of ',', due to the stored house, battery and cable data.
        format:
        total_costs (int value); houses ([x,y,maxoutput]); batteries ([x,y,capacity]); cables ([x_beign,y_begin,x_end,y_end])
        """
        ##text=List of strings to be written to file
        with open(f'data/results/district-{self.districtNumber}_alg{self.usedAlgorithmNumber}.csv','wb') as file:
            #write_houses = f'{houses}'
            file.write(f'{total_costs}; {houses}; {batteries}; {cables}')

    
    def ClearExperimentData(self):
        """
        Clears all data from a file for a hard reset, when significant changes are made.
        """
        with open(f'district-{self.districtNumber}_alg{self.usedAlgorithmNumber}.csv', 'r+') as file:
            # read one line (header)
            next(file)
            # delete everything below that (all data)
            file.truncate()
