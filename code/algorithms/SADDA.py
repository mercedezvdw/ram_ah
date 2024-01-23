# Rembrand Ruppert, Team RAM
# Smart Allocated Density Districts Algorithm (SADDA) (use (self built) K-means clustering algorithm to find 'sub-districts' / connects houses to the best possible battery)

from code.algorithms.DCA import DensityComputation
from code.classes.cable import CableSegment
import numpy as np
import random

class SADDA():
    def __init__(self, BatteryList, HouseList):
        """
        Initialise battery and house positions to use
        """
        self.BatteryPosList = BatteryList
        self.HousePosList = HouseList
        
        #print(self.BatteryPosList[0].position)
    
    def GetPosList(self):
        """
        Creates a mapping of house density using the assumption we use a 1x1 grid.
        """
        PosList = []
        # create a list of all x and y positions
        for i in range(len(self.HousePosList)):
            # [x, y]
            PosList.append([self.HousePosList[i].position[0], self.HousePosList[i].position[1]])
        
        #print(PosList)
        return PosList
    
    def GetCentroidPositions(self, PosList):
        """
        Forms as many centroids as there are batteries, places them randomly, finds the nearest houses to each centroid, reset centroid position based on houses around it
        """
        # go through every grid node and determine the local density using a simplified SPH code
        # density map is XxY of the grid of the map, but instead of [x, y] as value is has a value of [x, y, houses / (kernel rdaius)^2]
        HouseAllocation = []

        # find min and max x and y
        min_x = min(PosList)[0]
        min_y = min(PosList)[1]
        max_x = max(PosList)[0]
        max_y = max(PosList)[1]
        #print(all_x, all_y)
        #print(min_x, min_y, max_x, max_y)
        # define a square based on the biggest axix
        if (max_x - min_x) > (max_y - min_y):
            # make sure GridSize is an int
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
        #print(xCenter, yCenter, GridSize)
        # for every grid node position, calculate the local density
        xGridMin = int(xCenter - GridSize/2)+1
        yGridMin = int(yCenter - GridSize/2)+1
        xGridMax = GridSize + int(xCenter - GridSize/2)+1
        yGridMax = GridSize + int(yCenter - GridSize/2)+1
        #print("Minimum x,y:", xGridMin, yGridMin)
        #print("Maximum x,y:", xGridMax, yGridMax)

        # generate centroids randomly
        centroids = []
        numCentroids = len(self.BatteryPosList)
        for i in range(numCentroids):
            centroids.append([self.HousePosList[i].position[0], self.HousePosList[i].position[1]])

        # repeat the next step until there is no change, 42 is (ofcourse) the correct number of loops for this to have diminishing to no returns
        for _ in range(42):
            # calculate for every house which is the nearest centroid and then assign this position to that centroid
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
                #print((centroidAssignmentList))

            # recalculate the position of the centroid depending on all the houses that belong to it
            # for every centroid
            #print(centroids)
            for i in range(numCentroids):
                x_coord = 0
                y_coord = 0
                housesAssigned = 0
                # see which houses are assigned to this centroid and calculate avg position
                for j in range(len(centroidAssignmentList)):
                    if centroidAssignmentList[j][0] == i:
                        x_coord += centroidAssignmentList[j][1]
                        y_coord += centroidAssignmentList[j][2]
                        housesAssigned += 1
                        #print(x_coord, y_coord, housesAssigned)
                        
                x_coord = x_coord / housesAssigned
                y_coord = y_coord / housesAssigned

                # update position
                centroids[i][0] = x_coord
                centroids[i][1] = y_coord
        
            
        return centroids
    
    def GetHouseBatteryConnection(self, PosList, centroids):
        """
        Finds the best house-battery connection per house.
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
            connections[self.HousePosList[self.HBC[i][0]]] = self.BatteryPosList[self.HBC[i][1]]
        
        return connections

    def create_cable_route(self, start_position, end_position, houses, battery):
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
            

    
        return cable_route


    def check_battery_capacity(self, capacity, used_capacity, house_output):
        capacity = capacity - used_capacity - house_output
        return capacity


    def check_if_house(self, houses, cable_route):
        for route in cable_route[1:]:
            for house in houses.values():
                if house.position == route:
                    return house

    
    def SADDA_Run(self):
        """
        Runs the algorithm.
        """
        cable_routes = {}
        cables = {}
        sum_costs = 5000 * (len(self.BatteryPosList))

        for i in range(len(self.HBC)):
            connection = self.BatteryPosList[self.HBC[i][1]]
            cable_route = self.create_cable_route(self.HousePosList[self.HBC[i][0]].position, self.BatteryPosList[self.HBC[i][1]].position, self.HousePosList[self.HBC[i][0]], self.BatteryPosList[self.HBC[i][1]])
            #connection = battery.position
            #cable_route = self.create_cable_route(houses_posses[i].position, battery.position, houses_posses, battery)
            #self.HBC[i][0] = house number
            #self.HBC[i][1] = battery number

            route_costs = (len(cable_route) - 1) * 9
            cable_routes[i] = cable_route
            cables[i] = CableSegment(self.HousePosList[self.HBC[i][0]].position, connection, route_costs)
            sum_costs += route_costs

        print(f"The total price of the cables is {sum_costs}")
        return cables, cable_routes