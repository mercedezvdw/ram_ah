# Team RAM - Project SmartGrid
## Mercedez van der Wal // Rembrand Ruppert // Yessin Radouane

## Description
*Green energy is the energy of the future, and producing it yourself is the fashion of today. Many houses nowadays have solar panels, wind turbines or other installations to produce energy themselves. Fortunately, these installations often produce more than is needed for own consumption. The surplus could be sold back to the supplier, but the infrastructure (the grid) is often not designed for this. Batteries must be installed to manage peaks in consumption and production.
SmartGrid is a problem that describes a district with these houses and batteries placed on a grid. A solution to this problem is a scenario where all houses are connected to the batteries.*

## Requirements
*To run this program, the user needs to have a working version of python installed and download and unzip the 'ram_ah' folder.
After this, the user needs to install the required packages, listed in 'requirements.txt'.
The user now needs to open the 'ram_ah' directory in the preferred code editor.
Now, the user simply needs to type 'python main.py' into the command line and press enter, and the code will run.*


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






