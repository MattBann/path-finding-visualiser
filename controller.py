# Internal logic for the behavour of the control window

import threading
from typing import Callable

import pyglet
from pyglet.window import mouse

import pathfinding.dijkstras as dijkstras
import grid
import pathfinding.pathfinding_utils as pathfinding_utils
import pathfinding.a_star as a_star

# Grid dimensions
width, height = 50, 40

# Use foreground and background batch graphics processors to avoid layer issues
controller_batch_background = pyglet.graphics.Batch()
controller_batch_foreground = pyglet.graphics.Batch()

# Create hidden grid window. Allow resizing due to rendering issue, where only solution is to manually resize
grid_window = pyglet.window.Window(width=(width*10), height=(height*10), caption="Grid", visible=False, resizable=True )
new_grid = []

# Label definitions:
width_label = pyglet.text.Label(text=str(width), x=160, y=180, batch=controller_batch_foreground)
height_label = pyglet.text.Label(text=str(height), x=160, y=160, batch=controller_batch_foreground)
speed_label = pyglet.text.Label(text=str(pathfinding_utils.speed), x=160, y=200, batch=controller_batch_foreground)


def update_labels():
    width_label.text = str(width)
    height_label.text = str(height)
    speed_label.text = str(pathfinding_utils.speed)


# Click inside the grid window
@grid_window.event
def on_mouse_press(x, y, button, modifiers):
    grid_x, grid_y = x//10, y//10
    print(grid_x, grid_y) # For debugging
    # Validate that point is in grid
    if not (0 <= grid_x < width and 0<= grid_y < height):
        return
    if button == mouse.LEFT:
        new_grid[grid_x][grid_y].left_click_cell()
    elif button == mouse.RIGHT:
        new_grid[grid_x][grid_y].right_click_cell()
    elif button == mouse.MIDDLE:
        new_grid[grid_x][grid_y].middle_click_cell()


# Draw the grid window. Clear the screen then draw the cells
@grid_window.event
def on_draw():
    grid_window.clear()
    grid.grid_batch.draw()


# Close the grid window. Also called on control_window.on_close() in main. Exits the program
@grid_window.event
def on_close():
    grid_window.close()
    pyglet.app.exit()


# Class defining a button. Uses a rectangle for the shape and a label for the text
class Button:

    # Constructor. Takes position, size, text and a callable (function) used when clicked
    def __init__(self, x:int, y:int, width:int, height:int, text:str="", button_action:Callable=None) -> None:
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.action = button_action
        self.text = pyglet.text.Label(
            text, font_name="Arial", 
            batch=controller_batch_foreground, 
            anchor_x='center', anchor_y='center', 
            x=(x+width//2), y=(y+height//2), 
            color=(0,0,0,255),
            width=width,
            multiline=True
            )
        self.button_box = pyglet.shapes.Rectangle(x, y, width, height, color=(112, 213, 229), batch=controller_batch_background)
    

    def press_button(self):
        try:
            self.action()
        except:
            return -1


# Set the grids size and make it visible. 
def show_grid():
    if grid_window.visible:
        return
    global new_grid
    new_grid = grid.cells(width=width, height=height)
    grid_window.set_visible(True)
    grid_window.set_size(width*10, height*10)


# Incremental setters for speed with validation to keep within a range
def increase_speed():
    if pathfinding_utils.speed < 10 : pathfinding_utils.speed += 1
    update_labels()
def decrease_speed():
    if pathfinding_utils.speed > 1 : pathfinding_utils.speed -= 1
    update_labels()


# Incremental setters for width and height with validation to keep within a range
def increase_width():
    global width
    if width < 190: width+=1
    update_labels()
def decrease_width():
    global width
    if width > 4: width-=1
    update_labels()
def increase_height():
    global height
    if height < 100: height+=1
    update_labels()
def decrease_height():
    global height
    if height > 4: height-=1
    update_labels()


# Start running dijkstras algorithm in a seperate thread to allow grid to update as its running
def run_dijkstras():
    print("Running dijkstras")
    clear_grid()
    # a = threading.Thread(target=dijkstras.dijkstras_algorithm, args=(new_grid,), daemon=True)
    a = threading.Thread(target=a_star.a_star_algorithm, args=(new_grid,), daemon=True)
    a.start()


def clear_grid():
    grid.clear_grid(new_grid)


# Setters for the lambda function in pathfinding_utils.py that decides which directions can be moved in
def use_euclidean():
    pathfinding_utils.is_invalid = lambda i, j : i==0 and j==0

def use_manhattan():
    pathfinding_utils.is_invalid = lambda i, j : abs(i) == abs(j)


# Create and return a list of elements that a drawn inside the control window, including buttons and labels
def create_control_window():
    elements = []
    elements.append(Button(150, 130, 100, 20, "Create Grid", button_action=show_grid))
    elements.append(width_label)
    elements.append(pyglet.text.Label("Width", x=100, y=180, batch=controller_batch_foreground))
    elements.append(Button(200, 180, 40, 17, "Up", increase_width))
    elements.append(Button(250, 180, 40, 17, "Down", decrease_width))
    elements.append(Button(200, 160, 40, 17, "Up", increase_height))
    elements.append(Button(250, 160, 40, 17, "Down", decrease_height))
    elements.append(height_label)
    elements.append(pyglet.text.Label("Height", x=100, y=160, batch=controller_batch_foreground))
    elements.append(Button(160,10,80,20,"Dijkstras", run_dijkstras))
    elements.append(Button(160, 100, 80, 20, "Clear Grid", clear_grid))
    elements.append(Button(130, 70, 140, 20, "Use Euclidean", use_euclidean))
    elements.append(Button(130, 40, 140, 20, "Use Manhattan", use_manhattan))
    elements.append(Button(200, 200, 40, 17, "Up", increase_speed))
    elements.append(Button(250, 200, 40, 17, "Down", decrease_speed))
    elements.append(pyglet.text.Label("Speed", x=100, y=200, batch=controller_batch_foreground))

    return elements
