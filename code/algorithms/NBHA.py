# Rembrand Ruppert, Mercedez van der Wal, Yessin Radouane
# Nearest-Battery Heuristic Algorithm -- Shortest path to closest battery.
# For every house, check first if there is already a cable connected, to minimilize the costs of cables

import math

def calculate_distance(c1, c2):
    """
    Calculate the distance between two coordinates
    """
    distance = math.sqrt(((c1[0] - c2[0]) ** 2) + ((c1[1] - c2[1]) ** 2))
    return distance
    
def check_battery_capacity(capacity, used_capacity, house_output):
    capacity = capacity - used_capacity - house_output
    return capacity
    
def find_cable_path(target_position, cable_routes, batteries, house_output):
    for route in cable_routes.values():
        for coordinate in route:
            if coordinate == target_position:
                destination = route[-1]
                battery = find_battery(batteries, destination)
            
                if battery is not None:
                    check_capacity = check_battery_capacity(battery.capacity, battery.used_capacity, house_output)
                    if check_capacity > 0:
                        return battery
                        
def find_random_connection(cables, battery):
    """
    Find a random connection with a given battery
    """
    matching_house = None
    for cable in cables.values():
        if cable.pos_end == battery.position:
            matching_house = cable.pos_begin
            return matching_house
            
def find_cable_route(house_position, battery_position, cable_routes):
    i = 0
    for cable, route in cable_routes.items():
        if house_position in route:
            matching_cable = cable
            return matching_cable
            
def undo_connection(house, battery, cable_routes, assign_again):
    matching_cable = find_cable_route(house.position, battery.position, cable_routes)
    del cable_routes[matching_cable]
    battery.remove_used_capacity(house.max_output)
    assign_again.append(house)
    
                
def find_closest_battery(house, batteries: dict, cable_routes, cables, assign_again):
    """
    For each battery calculate the distance to find the closest battery
    """
    nearest_battery = None
    min_distance = float('inf')
    
    while True:
        max_capacity = 0
        battery_full = None
        
        for i in range(len(batteries)):
            
            # Check if battery has sufficient capacity
            capacity = batteries[i].capacity - batteries[i].used_capacity
            used_capacity = capacity - house.max_output
            
            if capacity > max_capacity:
                max_capacity = capacity
                battery_full = batteries[i]
        
            if used_capacity > 0:
                # Calculate distance and choose the battery with the closest distance
                distance = calculate_distance(house.position, batteries[i].position)
                if distance < min_distance:
                    min_distance = distance
                    nearest_battery = batteries[i]
            
        if nearest_battery is not None:
            return nearest_battery
        else:
            # If there is no battery left with sufficient capacity, undo random connection with battery that has most capacity left

            random_house = find_random_connection(cables, batteries[i])
            undo_connection(house, battery_full, cable_routes, assign_again)
            # Reset min_distance for the next iteration
            min_distance = float('inf')

def find_closest_cable(cable_routes, house_position, house_output, batteries, cables):
    min_distance = float('inf')
    closest_cable = None
    connected_battery = None

    for route in list(cable_routes.values())[1:-1]:
        for coordinate in route:
            old_min_distance = min_distance
            distance = calculate_distance(house_position, coordinate)
            destination = route[-1]
            start_position = route[0]
            
            if distance < min_distance:
                min_distance = distance
                closest_cable = coordinate
                
                # Check if it's a battery and if it has sufficient capacity
                battery = find_battery(batteries, closest_cable)
                if battery is not None:
                    check_capacity = check_battery_capacity(battery.capacity, battery.used_capacity, house_output)
                    connected_battery = battery
                    if check_capacity > 0:
                        return closest_cable, connected_battery
                            
                # If it is not a battery, find the connection to the battery
                battery = find_battery(batteries, destination)
                if battery is not None:
                    check_capacity = check_battery_capacity(battery.capacity, battery.used_capacity, house_output)
                    if check_capacity > 0:
                        connected_battery = battery
                        return closest_cable, connected_battery
                    else: 
                        min_distance = old_min_distance
                        closest_cable = None
                        connected_battery = None
                        continue       
                
                begin = destination
                
                # Keep going until you find the battery
                for route in list(cable_routes.values()):
                    if begin == route[0]:
                        end = route[-1]
                        battery = find_battery(batteries, end)
                        if battery is not None:
                            check_capacity = check_battery_capacity(battery.capacity, battery.used_capacity, house_output)
                            if check_capacity > 0:
                                connected_battery = battery
                                return closest_cable, connected_battery
                            else:
                                min_distance = old_min_distance
                                closest_cable = coordinate
                                connected_battery = None
                                break
                        else:
                            begin = end
    return None, None
    
def find_connected_battery(cables, closest_cable):
    for cable in cables.values():
        if cable.pos_begin == closest_cable:
            connected_battery = cable.pos_end
            return connected_battery
    return None
    
def find_battery(batteries, target_position):
    for battery in batteries.values():
        if battery.position == target_position:
                return battery
    return None
    
def find_house(houses, target_position):
    for house in houses.values():
        if house.position == target_position:
                return house
    return None
        
def compare_results(house_position, nearest_battery_position, closest_coordinate):
    """
    Compare the distance between the nearesty battery and choose shortest route
    """

    distance1 = calculate_distance(house_position, nearest_battery_position)
    distance2 = calculate_distance(house_position, closest_coordinate)
        
    if distance1 < distance2:
        return nearest_battery_position
    else: 
        return closest_coordinate
        
def check_if_house(houses, cable_route):
    for route in cable_route[1:]:
        for house in houses.values():
            if house.position == route:
                return house

def create_cable_route(start_position, end_position, houses, battery):
    """
    Create cable with shortest path (based on heuristics) from start to end position
    """
    steps_right = 0
    steps_left = 0
    steps_up = 0
    steps_down = 0
    current_position = start_position
    
    # Compare the x coordinates, to determine to go left or right
    if start_position[0] < end_position[0]:
        steps_right = end_position[0] - start_position[0]
    elif start_position[0] > end_position[0]:
        steps_left = start_position[0] - end_position[0]
    
    # Compare the y coordinates, to determine to go up or down
    if start_position[1] < end_position[1]:
        steps_up = end_position[1] - start_position[1]
    elif start_position[1] > end_position[1]:
        steps_down = start_position[1] - end_position[1]

    cable_route = [current_position.copy()]
    
    # Move on the y axis
    for i in range(steps_up):
        current_position = [current_position[0], current_position[1] + 1]
        cable_route.append(current_position.copy())
    for i in range(steps_down):
        current_position = [current_position[0], current_position[1] - 1]
        cable_route.append(current_position.copy())
    
    # Move on the x axis
    for i in range(steps_right):
        current_position = [current_position[0] + 1, current_position[1]]
        cable_route.append(current_position.copy())
    for i in range(steps_left):
        current_position = [current_position[0] - 1, current_position[1]]
        cable_route.append(current_position.copy())
        
    house = check_if_house(houses, cable_route)
    
    if house is not None:
        check_capacity = check_battery_capacity(battery.capacity, battery.used_capacity, house.max_output)
        if check_capacity < 0:
            AssertionError
   
    return cable_route