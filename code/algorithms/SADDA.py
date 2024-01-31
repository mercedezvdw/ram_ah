# Rembrand Ruppert, Team RAM
# Smart Allocated Density Districts Algorithm (SADDA) (use (self built) K-means clustering algorithm to find 'sub-districts' / connects houses to the best possible battery)

from code.classes.cable import CableSegment
import numpy as np
import random

class SADDA():
    def __init__(self, BatteryList, HouseList, seed):
        """
        Initialise battery and house positions to use
        """
        self.BatteryPosList = BatteryList
        self.HousePosList = HouseList
        random.seed(seed)
    

    def GetPosList(self):
        """
        Creates a mapping of house density using the assumption we use a 1x1 grid
        """
        PosList = []
        
        # Create a list of all x and y positions
        for i in range(len(self.HousePosList)):
            # [x, y]
            PosList.append([self.HousePosList[i].position[0], self.HousePosList[i].position[1]])
        
        return PosList
    

    def GetCentroidPositions(self, PosList):
        """
        Forms as many centroids as there are batteries, places them randomly, finds the nearest houses to each centroid, reset centroid position based on houses around it
        """
        # Go through every grid node and determine the local density using a simplified SPH code
        # density map is XxY of the grid of the map, but instead of [x, y] as value is has a value of [x, y, houses / (kernel rdaius)^2]
        HouseAllocation = []

        # Find min and max x and y
        min_x = min(PosList)[0]
        min_y = min(PosList)[1]
        max_x = max(PosList)[0]
        max_y = max(PosList)[1]

        # Define a square based on the biggest axis
        if (max_x - min_x) > (max_y - min_y):
            
            # Make sure GridSize is an int
            GridSize = int(max_x - min_x)
            minimum = min_x
            maximum = max_x
        else:
            GridSize = int(max_y - min_y)
            minimum = min_y
            maximum = max_y

        self.GridSize = GridSize

        minPos = []
        maxPos = []

        xCenter = int(min_x + (max_x - min_x)/2)
        yCenter = int(min_y + (max_y - min_y)/2)

        # For every grid node position, calculate the local density
        xGridMin = int(xCenter - GridSize/2)+1
        yGridMin = int(yCenter - GridSize/2)+1
        xGridMax = GridSize + int(xCenter - GridSize/2)+1

        # Generate centroids randomly
        centroids = []
        numCentroids = len(self.BatteryPosList)
        spawnedCentroids = 0

        # First I had centroids spawn on battery locations, but now we take random values of gridnodes of the system (0-50)
        # also check if the correct amount of centroids are spawned without some having the same initial position
        # (for loop -> while loop)
        while spawnedCentroids < numCentroids:
            coords = [int(random.random()*50), int(random.random()*50)]
            if coords not in centroids:
                centroids.append([int(random.random()*50), int(random.random()*50)])
                spawnedCentroids += 1

        # Repeat the next step until there is no change,
        # 42 is (ofcourse) the correct number of loops for this to have diminishing to no returns,
        # but 10 roughly disperses the capacity the best
        for _ in range(1,int(random.random()*420)):
    
            # Calculate for every house which is the nearest centroid and then assign this position to that centroid
            centroidAssignmentList = [] # [centroid number, x, y]
            for i in range(len(self.HousePosList)):
                distanceToCentroid = GridSize*2
                for j in range(numCentroids):
                    x = PosList[i][0] - centroids[j][0]
                    y = PosList[i][1] - centroids[j][1]
                    distance = (x**2 + y**2)**0.5
                    if distance < distanceToCentroid:
                        distanceToCentroid = distance
                        AssignedX = PosList[i][0]
                        AssignedY = PosList[i][1]
                        assignedCentroid = j
                centroidAssignmentList.append([assignedCentroid, AssignedX, AssignedY])

            # Recalculate the position of the centroid depending on all the houses that belong to it
            # for every centroid
            for i in range(numCentroids):
                x_coord = 0
                y_coord = 0
                housesAssigned = 0

                # See which houses are assigned to this centroid and calculate avg position
                for j in range(len(centroidAssignmentList)):
                    if centroidAssignmentList[j][0] == i:
                        x_coord += centroidAssignmentList[j][1]
                        y_coord += centroidAssignmentList[j][2]
                        housesAssigned += 1
                
                # Failsafe if no houses are assigned to a centroid
                # (should not be the case, but just to prevent errors)
                if housesAssigned > 0:
                    x_coord = x_coord / housesAssigned
                    y_coord = y_coord / housesAssigned

                # Update position
                centroids[i][0] = x_coord
                centroids[i][1] = y_coord

        return centroids
    

    def GetHouseBatteryConnection(self, PosList, centroids):
        """
        Finds the best house-battery connection per house
        """
        HBC = [] # [house number, what battery it should connect to]
        distanceToCentroid = self.GridSize*2

        # for every house, determine the best battery to use using the centroids
        for i in range(len(self.HousePosList)):
            for j in range(len(centroids)):

                x = PosList[i][0] - centroids[j][0]
                y = PosList[i][1] - centroids[j][1]
                distance = (x**2 + y**2)**0.5
                if distance < distanceToCentroid:
                    distanceToCentroid = distance
                    assignedBattery = j
            HBC.append([i, assignedBattery])

        self.HBC = HBC
        return HBC


    def calculate_distance(self, c1, c2):
        """
        Calculate the distance between two coordinates
        """
        distance = (((c1[0] - c2[0]) ** 2) + ((c1[1] - c2[1]) ** 2))**0.5
        return distance


    def make_connections(self):
        """
        Connect the houses to the closest battery
        format: {house object: battery object}
        """
        connections = {}

        for i in range(len(self.HBC)):            
            connections[i] = [self.HousePosList[self.HBC[i][0]].position, self.BatteryPosList[self.HBC[i][1]].position]

        return connections


    def create_cable_route(self, start_position, end_position, houses, battery, cable_routes):
        """
        Create cable with shortest path from start to end position
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
            if current_position not in cable_route:
                cable_route.append(current_position.copy())
        for i in range(steps_down):
            current_position = [current_position[0], current_position[1] - 1]
            if current_position not in cable_route:
                cable_route.append(current_position.copy())

        # Move on the x axis
        for i in range(steps_right):
            current_position = [current_position[0] + 1, current_position[1]]
            if current_position not in cable_route:
                cable_route.append(current_position.copy())
        for i in range(steps_left):
            current_position = [current_position[0] - 1, current_position[1]]
            if current_position not in cable_route:
                cable_route.append(current_position.copy())

        return cable_route


    def check_for_overlap(self, cable_routes):
        """
        Takes the original complete cable connections and eliminates duplicate/overlapping segment begin/end pos pairs
        """
        all_cable_segments = []

        # Store all [begin, end] pos coords
        for i in range(len(cable_routes.items())):
            for j in range(len(cable_routes[i])-1):
                all_cable_segments.append([cable_routes[i][j], cable_routes[i][j+1]])

        # Eliminate duplicates
        # check if a segment is used more than once,
        # if so, store this as a overlapping segment
        overlap_cable_segments = []
        for i in range(len(all_cable_segments)):
            local_segment = [all_cable_segments[i][0], all_cable_segments[i][1]]
            if all_cable_segments.count(local_segment) > 1:
                overlap_cable_segments.append(local_segment)

        # Remove duplicates in this list
        overlap_cable_segments = [i for n, i in enumerate(overlap_cable_segments) if i not in overlap_cable_segments[:n]]

        return overlap_cable_segments


    def check_battery_capacity(self, capacity, used_capacity, house_output):
        """
        Checks the capacity of the given battery
        """
        capacity = capacity - used_capacity - house_output
        return capacity


    def SADDA_Run(self):
        """
        Runs the algorithm
        """
        posses = self.GetPosList()
        centroids = self.GetCentroidPositions(posses)
        HBC = self.GetHouseBatteryConnection(posses, centroids)
        cable_routes = {}
        cables = {}
        sum_costs = 5000 * (len(self.BatteryPosList))

        for i in range(len(self.HBC)):
            # Makes the connection between houses and batteries,
            # determined by either the closest cable or the assigned battery
            # (closest cable still needs to be implemented)

            connection = self.BatteryPosList[self.HBC[i][1]]
            cable_route = self.create_cable_route(self.HousePosList[self.HBC[i][0]].position, self.BatteryPosList[self.HBC[i][1]].position, self.HousePosList[self.HBC[i][0]], self.BatteryPosList[self.HBC[i][1]], cable_routes)
            route_costs = (len(cable_route) - 1) * 9
            cable_routes[i] = cable_route
            self.BatteryPosList[self.HBC[i][1]].add_used_capacity(self.HousePosList[self.HBC[i][0]].max_output)
            sum_costs += route_costs

        #/ ------------------------ IMPORTANT ------------------------
        # Cables overlap, so check the cable segment lists to check where there are overlapping segments and remove all but 1
        # go through all routes and eliminate overlapping cables
        # and also recalc the price
        sum_costs = 5000 * (len(self.BatteryPosList))

        non_overlap_cable_routes = {}
        for N in range(len(self.BatteryPosList)):
            # To avoid overlap elimination for 2 cables that go to separate batteries,
            # reset used_segments after every battery is done connecting all cables
            used_segments = []
            
            for i in range(len(cable_routes)):
                # If the cable rout goes to the battery currently looked at,
                # only then do cable overlap elimination
                # cables to other batteries will come before or after this N loop
                if self.BatteryPosList[N].position == cable_routes[i][-1]:
                    route_list = []
                    route_list.append(cable_routes[i][0])
                    
                    for j in range(len(cable_routes[i])-1):
                        # Check if this segments has been used before,
                        # if not, place the segment and assign this to already used segments, so it cannot be used again
                        if ([cable_routes[i][j], cable_routes[i][j+1]] not in used_segments):
                            used_segments.append([cable_routes[i][j], cable_routes[i][j+1]])
                            route_list.append(cable_routes[i][j+1])
                            # Remove 9 for each segment removed
                            sum_costs += 9
                    non_overlap_cable_routes[i] = route_list

        print(f"The total price of the cables is {sum_costs}")
        connections = self.make_connections()

        return sum_costs, non_overlap_cable_routes, connections