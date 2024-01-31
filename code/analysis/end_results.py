import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_histogram_for_district(data_list, district_number, titles):
    plt.figure(figsize=(15, 5))

    for i, data in enumerate(data_list, 1):
        plt.subplot(1, len(data_list), i)

        # Filter data per district
        district_data = data[data['District Number'] == district_number]
        
        # Plot histogram
        plt.hist(district_data['Total Costs'], bins=20, edgecolor='black')
        plt.title(titles[i-1]) 
        plt.xlabel('Total costs')
        plt.ylabel('Frequency')
        plt.grid(True)

    plt.suptitle(f'District {district_number}')
    plt.tight_layout()
    plt.show()


base_path = 'data/algo_scores/'

algos = ['DFM', 'NBHA', 'Rv2', 'SADDA']
file_paths = [os.path.join(base_path, f'{algo}.csv') for algo in algos]
district_numbers = [1, 2, 3]

# Read data for each file
data_list = [pd.read_csv(file_path) for file_path in file_paths]

# Make histogram per file per district number
for district_number in district_numbers:
    titles = [f'Results for {algo}' for algo in algos]
    plot_histogram_for_district(data_list, district_number, titles)