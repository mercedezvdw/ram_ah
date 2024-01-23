# Rembrand Ruppert, Team RAM
# Writes the data stored in our own experiment datafiles

class WriteData():
    def __init__(self, districtNumber, usedAlgorithm):
        self.districtNumber = districtNumber
        self.usedAlgorithm = usedAlgorithm

    def WriteExperimentData(self, total_costs, houses, batteries, cables):
        """
        Writes the result of a single experiment in a csv file.
        The format we use splits the data using ; instead of ',', due to the stored house, battery and cable data.
        format:
        total_costs; houses; batteries; cables
        """
        ##text=List of strings to be written to file
        with open(f'district-{self.districtNumber}_alg{self.usedAlgorithm}.csv','wb') as file:
            file.write(f'{total_costs}; {houses}; {batteries}; {cables}')

    
    def ClearExperimentData(self):
        """
        Clears all data from a file for a hard reset, when significant changes are made.
        """
        with open(f'district-{self.districtNumber}_alg{self.usedAlgorithm}.csv', 'r+') as file:
            # read one line (header)
            next(file)
            # delete everything below that (all data)
            file.truncate()
