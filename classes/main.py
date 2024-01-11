# Mercedez van der Wal & Rembrand Ruppert
# Holds the class that defines a house in our case with its properties

# import all things needed
import matplotlib.pyplot as plt
import numpy as np
from house import House
from battery import Battery
from cable import CableSegment

# function to read the supplied CSV file
def ReadCSV():
    return


def DrawCase(GridSize):
    # plot grid lines
    for i in range(GridSize+1):
        plt.vlines(x = i, ymin = 0, ymax = GridSize, linestyles = ":", alpha = 0.5)
        plt.hlines(y = i, xmin = 0, xmax = GridSize, linestyles = ":", alpha = 0.5)
    # plot houses
    plt.plot()
    # plot batteries
    plt.plot()
    # plot cables
    plt.plot()
    # drawing details
    plt.xlim(-1,GridSize+1)
    plt.ylim(-1,GridSize+1)
    plt.legend()
    plt.tight_layout()
    plt.axis('scaled')
    # actuallly plot the thing
    plt.show()


DrawCase(10)