import matplotlib.pyplot as plt
import json
import numpy as np
import pandas as pd



def plot_top_scores():

    costs = {}

    for algo in ["DFM", "NBHA", "Rv2", "SADDA"]:
        algo_cost = {}
        for district in range(1,4):

            if district == 3 and algo == "DFM":
                break

            # read data
            file = open(f"data/results/district_{district}/district-{district}_{algo}.json")
            data = json.load(file)
            total_cost = data[0]["costs-shared"]

            # add to dict
            algo_cost[district] = total_cost


            # close file
            file.close()

        # add to dict
        costs[algo] = algo_cost

    tags = ('District 1', 'District 2', 'District 3')

    DFM = (costs["DFM"][1], costs["DFM"][2], 0)
    NBHA = (costs["NBHA"][1], costs["NBHA"][2], costs["NBHA"][3])
    RV2 = (costs["Rv2"][1], costs["Rv2"][2], costs["Rv2"][3])
    SADDA = (costs["SADDA"][1], costs["SADDA"][2], costs["SADDA"][3])

    # create a dataframe
    df = pd.DataFrame({"DFM": DFM, "NBHA": NBHA, "SADDA": SADDA, "RV2": RV2}, index=tags)
    df.plot.bar(rot=0, figsize=(12, 5))
    plt.tight_layout()
    plt.ylabel("Costs")
    plt.xlabel("District")
    plt.title("Costs per district per algorithm")
    plt.show()





plot_top_scores()