# Internal logic for the grid window

import math
import pyglet

grid_batch = pyglet.graphics.Batch()


# Class defining a grid cell. Adds extra properties to the BorderedRectangle class
class Cell(pyglet.shapes.BorderedRectangle):

    def __init__(self, x, y) -> None:
        super().__init__(x*10, y*10, 10, 10, batch=grid_batch)
        self.grid_x = x
        self.grid_y = y

        # Flags marking the status of a cell. Only one should be true at a time, if any
        self.is_start = False
        self.is_end = False
        self.is_wall = False

        # Useful properties for the pathfinding algorithms
        self.visited = False
        self.distance = math.inf
        self.previous_node : Cell = None
        

    def left_click_cell(self):
        # Cycle start end and clear
        self.is_wall = False
        if self.is_start:
            self.is_start = False
            self.is_end = True
        elif self.is_end:
            self.is_end = False
            self.is_start = False
        else:
            self.is_start = True
            self.is_end = False
        self.update_colours()
    

    def right_click_cell(self):
        # Toggle wall, if not start or finish
        if self.is_start or self.is_end:
            return
        self.is_wall = not self.is_wall
        self.update_colours()
    

    # For debugging, display information about a cell in the shell and update the cell's colour
    def middle_click_cell(self):
        print(f"About cell:\nVisited={self.visited}\nDistance from start={self.distance}")
        self.update_colours()
    

    # Change the cell's colour to represent its internal state
    def update_colours(self):
        if self.is_start:
            self.color = (0,0,255)
        elif self.is_end:
            self.color = (50, 225, 30)
        elif self.is_wall:
            self.color = (255,0,0)
        elif self.visited:
            self.color = (161, 185, 198)
        else:
            self.color = (255,255,255)
    

    # Temporarily set the colour to orange of itself and the previous node
    def visit_path(self):
        self.color = (234, 151, 7)
        if self.previous_node:
            self.previous_node.visit_path()
    

    # Force a call to update_colours on itself and the previous node
    def hide_path(self):
        self.update_colours()
        if self.previous_node:
            self.previous_node.hide_path()


    # Reset internal state, exluding start, end and wall status
    def clear(self):
        self.distance = math.inf
        self.visited = False
        self.previous_node = None
        self.update_colours()


# Create the grid with given width and height as a 2d array
def cells(width, height):
    grid = []
    for x in range(width):
        row = []
        for y in range(height):
            row.append(Cell(x,y))
        grid.append(row)
    
    return grid


def clear_grid(grid):
    for x in grid:
        for y in x:
            y.clear()