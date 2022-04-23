from grid import Cell

speed = 5
is_invalid = lambda i, j : i==0 and j==0

def get_adjacents(node : Cell, grid):
    adjacents = []
    # print(len(grid))
    # print(len(grid[0]))
    for i in -1, 0, 1:
        for j in -1, 0, 1:
            # print(node.grid_x+i,node.grid_y+j)
            # print((0 <= node.grid_x+i < len(grid)) and (0 <= node.grid_y+j < len(grid[0])))
            if is_invalid(i,j) or not (0 <= node.grid_x+i < len(grid) and 0 <= node.grid_y+j < len(grid[0])):
                continue
            found_node = grid[node.grid_x+i][node.grid_y+j]
            if found_node.is_wall:
                continue
            # print("Got node")
            adjacents.append(found_node)
    return adjacents