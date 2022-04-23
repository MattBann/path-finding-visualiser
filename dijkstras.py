import math
import time
import pathfinding_utils


def dijkstras_algorithm(grid: list):
    if not grid:
        print("No grid")
        return
    start_node = None
    end_node = None
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y].is_start and not start_node:
                start_node = grid[x][y]
                print(f"got start at {x}, {y}")
            elif grid[x][y].is_end and not end_node:
                end_node = grid[x][y]
                print("got end")
    
    if not start_node or not end_node:
        print("no start or end")
        return -1
    
    unvisited = []
    start_node.distance = 0
    current_node = start_node
    best_distance = math.inf
    running = True

    while running:
        current_node.visited = True
        adjacents = pathfinding_utils.get_adjacents(current_node, grid)
        
        for node in adjacents:
            new_distance = current_node.distance+math.sqrt((node.grid_x-current_node.grid_x)**2 + (node.grid_y-current_node.grid_y)**2)
            if node.distance > new_distance:
                node.distance = new_distance
                node.previous_node = current_node
                node.visit_path()
                if node == end_node:
                    best_distance = node.distance
                time.sleep(0.005 * (10-pathfinding_utils.speed))
                node.hide_path()
                

        for node in adjacents:
            if node not in unvisited and not node.visited:
                index = len(unvisited)
                for i in range(len(unvisited)):
                    if unvisited[i].distance > node.distance:
                        index = i
                        break
                unvisited.insert(index, node)

        current_node.update_colours()
        if len(unvisited) == 0:
            running = False
        else:
            current_node = unvisited.pop(0)
            if current_node.distance > best_distance:
                running = False
    
    print("Finished")
    end_node.visit_path()
    