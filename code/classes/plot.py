# Rembrand Ruppert, Team RAM
# Plots the district along with the placed cables

import matplotlib.pyplot as plt
import numpy as np
import random

class PlotCase():
    def __init__(self, batteries, houses, extraGridSpace, cable_routes, connections):
        """
        Initialsize all variables needed to plot a district map
        """
        self.batteries = batteries
        self.houses = houses
        self.extraGridSpace = extraGridSpace
        self.cable_routes = cable_routes
        self.connections = connections
        self.battery_colors = {}
    
    def AssignBatteryColors(self):
        """
        Assign colors to each battery
        """
        battery_colors = {}
        colors = ['deepskyblue', 'darkorange', 'forestgreen', 'deeppink', 'mediumpurple']
        i = 0
        
        for battery in self.batteries.values():
            x = tuple(battery.position)
            battery_colors[x] = colors[i]
            i += 1
        
        return battery_colors

    def DrawCase(self):
        """
        Draws a map of the chosen district showing all houses, battries and cables

        NOTE: cables argument is not used!
        """
        # Create a merged list of all positions and get the minimum and maximum x and y values to make a map
        # Add all x and y to respective lists
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

        # Find min and max x and y
        min_x = min(all_x)
        min_y = min(all_y)
        max_x = max(all_x)
        max_y = max(all_y)

        # Define a square based on the biggest axix
        if (max_x - min_x) > (max_y - min_y):
            
            # Make sure GridSize is an int
            GridSize = int(max_x - min_x)
            minimum = min_x
            maximum = max_x
        else:
            GridSize = int(max_y - min_y)
            minimum = min_y
            maximum = max_y

        xCenter = int(min_x + (max_x - min_x)/2)
        yCenter = int(min_y + (max_y - min_y)/2)

        # Plot grid lines
        for i in range(-self.extraGridSpace, GridSize+1 +self.extraGridSpace):
            # I used int()+1 so it is rounded up, int always rounds down
            plt.vlines(x = i + int(xCenter - GridSize/2)+1, ymin = int(yCenter - GridSize/2)+1-5, ymax = int(yCenter + GridSize/2)+1+5, linestyles = "-", linewidth=0.666, alpha = 0.1, zorder=-1)
            plt.hlines(y = i + int(yCenter - GridSize/2)+1, xmin = int(xCenter - GridSize/2)+1-5, xmax = int(xCenter + GridSize/2)+1+5, linestyles = "-", linewidth=0.666, alpha = 0.1, zorder=-1)
        
        # Delete labels from x and y axis
        plt.xticks([])
        plt.yticks([])
        
        battery_colors = self.AssignBatteryColors()
        
        # Plot houses
        if self.connections is not None:
            for i in range(len(self.houses)):
                for key, connection in self.connections.items():
                    if self.houses[i].position in connection:
                        batt = tuple(connection[1])
                        color = battery_colors[batt]
                plt.scatter(self.houses[i].position[0], self.houses[i].position[1], s = 30, color = color, marker = '^', label = 'house', zorder=1)
        
        else:
            for i in range(len(self.houses)):
                plt.scatter(self.houses[i].position[0], self.houses[i].position[1], s = 30, color = 'r', marker = '^', label = 'house', zorder=1)
            
        # Plot batteries
        for coord, color in battery_colors.items():
            plt.scatter(coord[0], coord[1], s = 55, color = color, marker = ',', label = 'battery', zorder = 1)
                
        
        # Plot cables
        if self.connections is not None:
            for key, route in self.cable_routes.items():
                if route != []:
                    x, y = zip(*route)
                    batt = tuple(self.connections[key][1])
                    color = battery_colors[batt]
                    plt.plot(x, y, color=color, linewidth=0.666, zorder=0)
        
        else:
            for key, route in self.cable_routes.items():
                x, y = zip(*route)
                plt.plot(x, y, color='b', linewidth=0.666, zorder=0)
        
        # Drawing details
        plt.xlim(-1,GridSize+1)
        plt.ylim(-1,GridSize+1)
        
        plt.tight_layout()
        plt.axis('scaled')
        
        # Actuallly plot the thing
        plt.show()
