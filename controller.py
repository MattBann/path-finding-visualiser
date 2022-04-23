import threading
from pyglet.window import mouse
from typing import Callable
import pyglet
import dijkstras, pathfinding_utils
import grid

width, height = 50, 40

controller_batch_background = pyglet.graphics.Batch()
controller_batch_foreground = pyglet.graphics.Batch()

grid_window = pyglet.window.Window(width=(width*10), height=(height*10), caption="Grid", visible=False, resizable=True )
new_grid = []

# Label definitions:
width_label = pyglet.text.Label(text=str(width), x=110, y=180, batch=controller_batch_foreground)
height_label = pyglet.text.Label(text=str(height), x=110, y=160, batch=controller_batch_foreground)

def update_labels():
    width_label.text = str(width)
    height_label.text = str(height)

@grid_window.event
def on_mouse_press(x, y, button, modifiers):
    grid_x, grid_y = x//10, y//10
    print(grid_x, grid_y)
    if button == mouse.LEFT:
        new_grid[grid_x][grid_y].left_click_cell()
    elif button == mouse.RIGHT:
        new_grid[grid_x][grid_y].right_click_cell()
    elif button == mouse.MIDDLE:
        new_grid[grid_x][grid_y].middle_click_cell()


# @grid_window.event
def on_draw():
    grid_window.clear()
    grid.grid_batch.draw()
    # print("Grid redrawn")

grid_window.on_draw = on_draw

@grid_window.event
def on_close():
    grid_window.close()
    pyglet.app.exit()


class Button:
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
            color=(255,0,0,255),
            width=width,
            multiline=True
            )
        self.button_box = pyglet.shapes.Rectangle(x, y, width, height, color=(153,153,153), batch=controller_batch_background)
    

    def press_button(self):
        try:
            self.action()
        except:
            return -1


def show_grid():
    if grid_window.visible:
        return
    global new_grid
    new_grid = grid.cells(width=width, height=height)
    grid_window.set_visible(True)
    grid_window.set_size(width*10, height*10)
    grid_window.clear()
    grid.grid_batch.draw()
    
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

def run_dijkstras():
    print("Running dijkstras")
    clear_grid()
    a = threading.Thread(target=dijkstras.dijkstras_algorithm, args=(new_grid,), daemon=True)
    a.start()
    # dijkstras.dijkstras_algorithm(new_grid)

def clear_grid():
    grid.clear_grid(new_grid)

def use_euclidean():
    pathfinding_utils.is_invalid = lambda i, j : i==0 and j==0

def use_manhattan():
    pathfinding_utils.is_invalid = lambda i, j : abs(i) == abs(j)

def create_control_window():
    elements = []
    elements.append(Button(150, 130, 100, 20, "Create Grid", button_action=show_grid))
    elements.append(width_label)
    elements.append(pyglet.text.Label("Width", x=50, y=180, batch=controller_batch_foreground))
    elements.append(Button(150, 180, 40, 15, "Up", increase_width))
    elements.append(Button(200, 180, 40, 15, "Down", decrease_width))
    elements.append(Button(150, 160, 40, 15, "Up", increase_height))
    elements.append(Button(200, 160, 40, 15, "Down", decrease_height))
    elements.append(height_label)
    elements.append(pyglet.text.Label("Height", x=50, y=160, batch=controller_batch_foreground))
    elements.append(Button(160,10,80,20,"Dijkstras", run_dijkstras))
    elements.append(Button(160, 100, 80, 20, "Clear Grid", clear_grid))
    elements.append(Button(130, 70, 140, 20, "Use Euclidean", use_euclidean))
    elements.append(Button(130, 40, 140, 20, "Use Manhattan", use_manhattan))


    return elements