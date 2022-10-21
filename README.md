# Path finding visualiser

A visualisation tool for path-finding algorithms, written in python.

## Requirements

 - Pyglet python library. This can be installed using
 
     python3 -m pip install pyglet --user

## Usage

Run main.py using python 3:

    python3 main.py

You will be greeted by a menu with a number of options:

 - Speed is the speed at which the algorithm runs. 10 is near instant, while 1 is slow enough to see each node being tested
 - Width and height are the dimensions of the grid. Be aware that changing these after creating the grid will have no effect

Change the above values by clicking the up or down buttons next to them. To increase/decrease by 5 at a time, hold shift.

Click 'Create Grid' to open a new window showing the grid:
 - Left click a tile to cycle its state between start point (blue), end point (green) or empty (white). If multiple tiles are marked as the start or end, only one will be used
 - Right click an empty tile to set it as a wall. Drag with right click to set multiple tiles as walls

The 'Clear Grid' button resets the grid after an algorithm is run, though doesn't change the start point, end point, or walls. 

There also buttons to select the type of geometry the system can use, which will affect the shape of the path:
 - Euclidian means diagonals are allowed, though the distance to one is greater than an immediate neighbour (i.e. it uses pythagoras)
 - Manhattan means only immediate (non diagonal) neighbours are allowed, forcing it to use a 'Manhattan distance', so called because of the grid nature of Manhattan's map

Once all options are set, and start/end nodes selected, click one of the algorithms to start it, and watch it play out on the grid.

## Algorithms

You can choose between Dijkstra's Algorithm and the A* Algorithm. Both follow the principal of exploring neighbouring cells in order of their score.
For Dijkstra, this score is just the distance to a cell from the start point through the best path. This causes it to naivly explore radially in all directions when unobstructed.
The score in A* is the sum of the distance to a cell from the start point through the best path and a heuristic (estimated) distance from the cell to the end point. Here, the heuristic is Euclidian distance (i.e. straight line distance) or Manhatten distance (difference in x plus difference in y). This results in the algorithm having a sense of direction, unlike in Dijkstras, which also causes it to generally find a solution faster.
