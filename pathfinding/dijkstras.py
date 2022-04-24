# Implementation of Dijkstra's Algorithm
# This is independant of the visualiser and could theoretically be used on its own with a grid of cell-like objects

import math
import time
import pathfinding.pathfinding_utils as pathfinding_utils


def dijkstras_algorithm(grid):
    
    # Validate that a grid was given
    if not grid or grid == []:
        print("No grid")
        return

    # Get start and end node
    start_node = None
    end_node = None
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y].is_start and not start_node:
                start_node = grid[x][y]
                print(f"Got start at {x}, {y}")
            elif grid[x][y].is_end and not end_node:
                end_node = grid[x][y]
                print(f"Got end at {x}, {y}")
    
    if not start_node or not end_node:
        print("No start or no end")
        return -1
    
    # Initialise variables
    unvisited = []
    start_node.distance = 0
    current_node = start_node
    best_distance = math.inf
    running = True

    # Main loop
    while running:

        # Visit node
        current_node.visited = True
        adjacents = pathfinding_utils.get_adjacents(current_node, grid)
        
        # Update distance to each neighbouring unvisited node
        for node in adjacents:
            if node.visited: continue
            new_distance = current_node.distance+math.sqrt((node.grid_x-current_node.grid_x)**2 + (node.grid_y-current_node.grid_y)**2)
            if node.distance > new_distance:
                node.distance = new_distance
                node.previous_node = current_node
                node.visit_path()
                if node == end_node:
                    best_distance = node.distance
                # Artificially slow down execution to allow grid window to show path being visited
                time.sleep(0.005 * (10-pathfinding_utils.speed))
                node.hide_path()
                
        # Use insertion sort to add newly discovered unvisted nodes to unvisited list in distance order
        for node in adjacents:
            if node not in unvisited and not node.visited:
                index = len(unvisited)
                for i in range(len(unvisited)):
                    if unvisited[i].distance > node.distance:
                        index = i
                        break
                unvisited.insert(index, node)

        current_node.update_colours()

        # If all accessible nodes exausted, stop, else visit the next closest node
        if len(unvisited) == 0:
            running = False
        else:
            current_node = unvisited.pop(0)
            if current_node.distance > best_distance:
                running = False
    
    print("Finished")
    end_node.visit_path()
    