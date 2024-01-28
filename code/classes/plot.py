# Rembrand Ruppert, Team RAM
# Plots the district along with the placed cables

import matplotlib.pyplot as plt
import numpy as np
import random
from code.algorithms.randomise import *
from code.algorithms.DCA import DensityComputation

class PlotCase():
    def __init__(self, batteries, houses, extraGridSpace, cable_routes):
        """
        Initialsize all variables needed to plot a district map
        """
        self.batteries = batteries
        self.houses = houses
        self.extraGridSpace = extraGridSpace
        self.cable_routes = cable_routes


    def DrawCase(self):
        """
        Draws a map of the chosen district showing all houses, battries and cables

        NOTE: cables argument is not used!
        """
        # calculate a density mapping of all houses in the district
        #DCA = DensityComputation(self.batteries, self.houses)
        #PosList = DCA.GetPosList()
        #DensityMap = DCA.GetDensityMapping(PosList, self.extraGridSpace)
        #DensityMap = DCA.AlterGrid(DensityMap)
        # make DensityMap a numpy array to use more efficiently
        #DensityMap = np.array(DensityMap)

        # create a merged list of all positions and get the minimum and maximum x and y values to make a map
        # add all x and y to respective lists
        all_x = []
        all_y = []
        for i in range(len(self.batteries)):
            all_x.append(self.batteries[i].position[0])
        for i in range(len(self.batteries)):
            all_y.append(self.batteries[i].position[1])
        for i in range(len(self.houses)):
            all_x.append(self.houses[i].position[0])
        for i in range(len(self.houses)):
            all_y.append(self.houses[i].position[1])

        # find min and max x and y
        min_x = min(all_x)
        min_y = min(all_y)
        max_x = max(all_x)
        max_y = max(all_y)

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

        xCenter = int(min_x + (max_x - min_x)/2)
        yCenter = int(min_y + (max_y - min_y)/2)

        # plot density map
        #cmap = plt.set_cmap('inferno')
        #plt.scatter(DensityMap[:, 0:1], DensityMap[:, 1:2], c=DensityMap[:, 2:3], cmap=cmap, marker=',', s=55, alpha=1, zorder=-2)
        #plt.colorbar()

        # plot grid lines
        for i in range(-self.extraGridSpace, GridSize+1 +self.extraGridSpace):
            # I used int()+1 so it is rounded up, int always rounds down
            plt.vlines(x = i + int(xCenter - GridSize/2)+1, ymin = int(yCenter - GridSize/2)+1-5, ymax = int(yCenter + GridSize/2)+1+5, linestyles = "-", alpha = 0.33, zorder=-1)
            plt.hlines(y = i + int(yCenter - GridSize/2)+1, xmin = int(xCenter - GridSize/2)+1-5, xmax = int(xCenter + GridSize/2)+1+5, linestyles = "-", alpha = 0.33, zorder=-1)
        # plot houses
        for i in range(len(self.houses)):
            plt.scatter(self.houses[i].position[0], self.houses[i].position[1], s = 75, color = 'r', marker = '^', label = 'house', zorder=1)
        # plot batteries
        for i in range(len(self.batteries)):
            plt.scatter(self.batteries[i].position[0], self.batteries[i].position[1], s = 75, color = 'g', marker = ',', label = 'battery', zorder=1)

        # Plot cables
        for key, route in self.cable_routes.items():
            x, y = zip(*route)
            plt.plot(x, y, color='b', zorder=0)
        
        # drawing details
        plt.xlim(-1,GridSize+1)
        plt.ylim(-1,GridSize+1)
        #plt.legend()
        
        plt.tight_layout()
        plt.axis('scaled')
        # actuallly plot the thing
        plt.show()
