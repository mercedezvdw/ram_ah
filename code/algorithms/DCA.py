# Rembrand Ruppert, Team RAM
# Density Computing Algorithm (DCA) (uses either KNN or altered SPH density calculations / compute house density and create subdistricts)
# Use grid node system to find density across nodes.

import numpy as np

class DensityComputation():
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
    
    def GetDensityMapping(self, PosList, extraGridSpace):
        """
        Creates a mapping of house density using the assumption we use a 1x1 grid.
        """
        # go through every grid node and determine the local density using a simplified SPH code
        # density map is XxY of the grid of the map, but instead of [x, y] as value is has a value of [x, y, houses / (kernel rdaius)^2]
        kernelRadius = (2)**0.5
        DensityMap = []

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

        # loop over all nodes
        for i in range(xGridMin-extraGridSpace, xGridMax+1+extraGridSpace):
            for j in range(yGridMin-extraGridSpace, yGridMax+1+extraGridSpace):
                # calculate density using all houses
                DensityValue = 0
                for k in range(len(self.HousePosList)):
                    houseLocation = [self.HousePosList[k].position[0], self.HousePosList[k].position[1]]
                    localNode = [i,j]
                    x = abs(houseLocation[0] - localNode[0])
                    y = abs(houseLocation[1] - localNode[1])
                    distance = ((x)**2 + (y)**2)**0.5
                    DensityValue += np.exp(-(distance**2)/(4))

                DensityMap.append([i,j,DensityValue])
        #print(DensityMap)

        return DensityMap
    
    def AlterGrid(self, DensityMap):
        """
        Alters the existing density map to a 0 or 1 density per node to make dividing sub-districts easier
        """
        NewDensityMap = []
        DensityMap = np.array(DensityMap)

        # determine standard deviation of the density map
        std = np.std(DensityMap[:, 2:3])

        # loop through current denisty map and using the std value, alter everything above to 1 and everything below to 0
        for i in range(len(DensityMap)):
            value = DensityMap[i][2]
            if value > std:
                NewValue = 1
            else:
                NewValue = 0
            NewDensityMap.append([DensityMap[i, 0:1], DensityMap[i, 1:2],NewValue])


        return NewDensityMap

    def GetSubDistricts(self):
        """
        When viewing the density map, it was clear this method could not be used efficiently, due to many subdistricts still being connected
        due to the house placement.
        I have now switched over to SADDA, wich should work better.
        """


'''
# for plotting in plot.py:

    DCA = DensityComputation(batteries, houses)
    PosList = DCA.GetPosList()
    DensityMap = DCA.GetDensityMapping(PosList, extraGridSpace)
    # make DensityMap a numpy array to use more efficiently
    DensityMap = np.array(DensityMap)

    ...
    
    # plot density map
    cmap = plt.set_cmap('inferno')
    plt.scatter(DensityMap[:, 0:1], DensityMap[:, 1:2], c=DensityMap[:, 2:3], cmap=cmap, marker=',', s=55, alpha=1, zorder=-2)
    plt.colorbar()
'''