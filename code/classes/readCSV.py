# Rembrand Ruppert, Team RAM
# function to read the supplied CSV files

from code.classes.house import House
from code.classes.battery import Battery

class CSVReader():
    def __init__(self, district_number):
        """
        Initialises what district to read
        """
        self.district_number = district_number


    def ReadCSV(self):
        """
        Reads the supplied .csv-files and stores the data in objects.
        """
        # Create lists to store data in and a row variable to use to read file
        battery_row = 0
        house_row = 0
        batteries = {}
        houses = {}

        # Read both files
        input_file_batteries = open(f'data/district_{self.district_number}/district-{self.district_number}_batteries.csv', 'r')
        input_file_houses = open(f'data/district_{self.district_number}/district-{self.district_number}_houses.csv', 'r')

        # Go through all rows and store data into lists
        for row_count in input_file_batteries:
            if battery_row > 0:
                row_count = row_count.strip()
                if '"' in row_count:
                    row_count = row_count.replace('"','')
                data_split = row_count.split(',')

                batteries[battery_row-1] = Battery([int(data_split[0]), int(data_split[1])], float(data_split[2]))
            battery_row += 1

        input_file_batteries.close()

        for row_count in input_file_houses:
            if house_row > 0:
                row_count = row_count.strip()
                data_split = row_count.split(',')
                houses[house_row-1] = House([int(data_split[0]), int(data_split[1])], float(data_split[2]))
            house_row += 1

        input_file_houses.close()

        return batteries, houses
