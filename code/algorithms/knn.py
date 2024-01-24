
def load_data():
    with open('../data/district_1/district-1_batteries.csv') as f:
        batteries = f.readlines()
        print(batteries)

def parse_position(pos_str):
    x, y = map(int, pos_str.split(','))
    return x, y

def calculate_distance(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

def assign_districts(batteries, houses):
    districts = []

    for house in houses:
        house_pos = (house['x'], house['y'])
        nearest_battery = min(
            batteries, 
            key=lambda battery: calculate_distance(house_pos, parse_position(battery['positie']))
        )
        districts.append({'house': house, 'battery': nearest_battery})

    return districts

def plot_districts(districts):
    # This function will plot the districts
    # Implementation will be added in the next step
    pass

# Load the data
# batteries, houses = load_data()
load_data()

# Assign districts
# districts = assign_districts(batteries, houses)

# # Plot the results
# plot_districts(districts)