# Team RAM - Project SmartGrid
## Mercedez van der Wal // Rembrand Ruppert // Yessin Radouane

## Description
*Green energy is the energy of the future, and producing it yourself is the fashion of today. Many houses nowadays have solar panels, wind turbines or other installations to produce energy themselves. Fortunately, these installations often produce more than is needed for own consumption. The surplus could be sold back to the supplier, but the infrastructure (the grid) is often not designed for this. Batteries must be installed to manage peaks in consumption and production.
SmartGrid is a problem that describes a district with these houses and batteries placed on a grid. A solution to this problem is a scenario where all houses are connected to the batteries.*

## Requirements
To run this program, the user needs to have a working version of python installed and download and unzip the 'ram_ah' folder.
After this, the user needs to install the required packages, listed in 'requirements.txt'.
The user now needs to open the 'ram_ah' directory in the preferred code editor.
Now, the user simply needs to type 'python main.py' into the command line and press enter, and the code will run.*

## Running the Algorithms with argparse
Argparse has been implemented for running `main.py`. For additional information, you can use `--help`. 
To run an algorithm use `--algo "name_algorithm" --district "district_number"`. Optional: use `--plot` to make a plot of the results.

Here's an example how it works:
```python3 main.py --algo SADDA --district 1 --plot`

## 15-01-2024 Notes of algorithm ideas

KNN Algorithm to divide neighborhoods and find closest battery
Density of houses (SPH-like); main cable with small(er) branches to closeby houses

Algorithms:
- Average Location Detection Algorithm (ALDA) ( find average location of all houses (within sub-districts) to batteries / calculate average amount of cables / maybe use it as regression to find approximate (main) cable location)
- Density Computing Algorithm (DCA) (uses either KNN or altered SPH density calculations / compute house density and create subdistricts)
- Random Walk Algorithm (RWA) (3 directions possible every step / max coordinates based on district size / no overlaying cables (two segments with the same begin and ending coords))
- Nearest Neighbour Algorithm (NNA) (from Nth house to nearest battery or cable segment / use different combinations of houses to find optimal minimum cable length / is like KNN, but oversimplified and self made)
- Smart Allocated Density Districts Algorithm (SADDA) (use (self built) KNN Algorithm to find 'sub-districts' / place a main cable through the highest density of a sub-district)

evaluation: amount of meters used for cables.

extra constraint: capacity

Use grid node system to find density across nodes.



## Best results after 10k iterations for each algo on each district

In the last weeks we have worked on 4 different algorithms to find an optimal solution for connecting houses with given batteries while respecting the maximum capacities of the batteries.
After running many iterations we have stored the best runs and their data. These were the best results in 10k iterations:

- ### Random v2 Algorithm (Rv2):
    ![Rv2](documentation/Rv2_MD.png)
    - Best score district 1: 98242
    - Best score district 2: 86299
    - Best score district 3: 90871

    This algorithm is our baseline. It connects houses to a battery and chooses a semi-random path to it. As you can see the costs are all very high and it is not guaranteed that batteries will not overload. Not the best way to connect the houses it shows.

- ### Smart Allocated Density Districts Algorithm (SADDA)
    ![SADDA](documentation/SADDA_MD.png)
    - Best score district 1: 36781
    - Best score district 2: 37132
    - Best score district 3: 37402

    As you can see this is a very consistent algorithm. It works good on all districts and has very respectable costs. With the datapoints we have gathered it seems to get more expensive over the districts. We suspect this is because the algorithm finds more complexity in district 3 than district 2. Both of these seem more complex than district 1.

- ### Nearest-Battery Heuristic Algorithm (NBHA)
    ![NBHA](documentation/NBHA_MD.png)
    - Best score district 1: 44161
    - Best score district 2: 40507
    - Best score district 3: 39175

    This is another well working algorithm. It works on all districts. This algorithm seems to work better in districts where SADDA finds more complexity. Although SADDA still performs slightly better. It yields around half the cost of the baseline while also ensuring batteries are not overloading.

- ### Depth-First Mycelium Algorithm (DFM)
    ![DFM](documentation/DFM_MD.png)
    - Best score district 1: 35332
    - Best score district 2: 34414
    - Best score district 3: x

    This algorithm seems to perform the best out of the others on district 1 and 2. It uses a depth-first like approach to find the paths. Though, it fails to find a way to connect the houses while respecting battery capacities. It can possibly be improved by adding more layers in depth.


Conclusion:
    We have created algorithms that have at least 2x the efficiency than our base algorithm in every district. We are happy with the progress we made.








