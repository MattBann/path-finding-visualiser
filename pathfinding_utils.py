# Useful variables and functions that are used by path-finding algorithms

from grid import Cell

# Number representing execution speed
speed = 5

# Simple function that can be switched by the control menu.
# Defines whether a direction is valid (e.g. diagonal movement is allowed by default) 
is_invalid = lambda i, j : i==0 and j==0


# Return a list containing all the cells adjacent to a given cell node.
# May or may not include diagonals depending on is_invalid
def get_adjacents(node : Cell, grid):
    adjacents = []
    # Iterate through each cardinal direction
    for i in -1, 0, 1:
        for j in -1, 0, 1:
            # Ignore invalid directions (always including (0,0)) and edges of the grid
            if is_invalid(i,j) or not (0 <= node.grid_x+i < len(grid) and 0 <= node.grid_y+j < len(grid[0])):
                continue
            found_node = grid[node.grid_x+i][node.grid_y+j]
            # Ignore walls
            if found_node.is_wall:
                continue
            adjacents.append(found_node)
    return adjacents