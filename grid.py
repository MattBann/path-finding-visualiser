import math
import pyglet

grid_batch = pyglet.graphics.Batch()

class Cell(pyglet.shapes.BorderedRectangle):

    def __init__(self, x, y) -> None:
        super().__init__(x*10, y*10, 10, 10, batch=grid_batch)
        self.is_start = False
        self.is_end = False
        self.is_wall = False
        self.grid_x = x
        self.grid_y = y

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
    
    def middle_click_cell(self):
        print(f"About cell:\nVisited={self.visited}\nDistance from start={self.distance}")
        self.update_colours()
    
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
    
    def visit_path(self):
        self.color = (234, 151, 7)
        if self.previous_node:
            self.previous_node.visit_path()
    
    def hide_path(self):
        self.update_colours()
        if self.previous_node:
            self.previous_node.hide_path()

    def clear(self):
        self.distance = math.inf
        self.visited = False
        self.previous_node = None
        self.update_colours()

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