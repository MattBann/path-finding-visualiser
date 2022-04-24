from pyglet.window import mouse, key
import pyglet
import controller

control_window = pyglet.window.Window(width=400, height=220, caption="Control")

# List of elements in the control window
control_window_elements = controller.create_control_window()

# Returns true if the point (x,y) is within the bounds of an object
def is_point_on_object(x, y, object):
    try:
        return object.x+object.width>x>object.x and object.y+object.height>y>object.y
    except:
        return False


# Click inside the control window. Find the object clicked on and try to call it's press_button() method
@control_window.event
def on_mouse_press(x, y, button, modifiers):
    for element in control_window_elements:
        if is_point_on_object(x, y, element):
            try:
                element.press_button()
                if modifiers & key.MOD_SHIFT and (element.text.text == "Up" or element.text.text == "Down"):
                    print("Shifted")
                    for i in range(4):
                        element.press_button()
                return
            except:
                continue


# Draw the control window. Clear the screen then draw the background and foreground elements
@control_window.event
def on_draw():
    control_window.clear()
    controller.controller_batch_background.draw()
    controller.controller_batch_foreground.draw()
    # print("Control redrawn")


# Close the control window. Pass through to controller.py which stops execution
@control_window.event
def on_close():
    controller.on_close()


# Dummy method needed to allow the screen to regularly redraw
def update(dt):
    pass

if __name__ == "__main__":
    # Start the clock that causes the screens to redraw at 30fps and run the app
    pyglet.clock.schedule_interval(update, 1/30)
    pyglet.app.run()
