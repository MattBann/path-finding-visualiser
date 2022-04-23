from pyglet.window import mouse, key
import pyglet
import controller

control_window = pyglet.window.Window(width=400, height=240, caption="Control")

control_window_elements = controller.create_control_window()

def is_point_on_object(x, y, object):
    try:
        return object.x+object.width>x>object.x and object.y+object.height>y>object.y
    except:
        return False


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
            except:
                continue


@control_window.event
def on_draw():
    control_window.clear()
    controller.controller_batch_background.draw()
    controller.controller_batch_foreground.draw()
    # print("Control redrawn")


@control_window.event
def on_close():
    controller.on_close()


def update(dt):
    pass

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1/30)
    pyglet.app.run()
