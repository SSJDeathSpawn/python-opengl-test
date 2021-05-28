#input/input_handler.py
import glfw

class InputHandler(object):
    def __init__(self):
        self.input_calls = []
        self.keys = [False for i in range(glfw.KEY_LAST)]

    def subscribe(self, func):
        self.input_calls.append(func)

    def handle_input(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            self.keys[key] = True
        elif action == glfw.RELEASE:
            self.keys[key] = False
        [i(window, key, scancode, action, mods) for i in self.input_calls]

    def unsubscribe(self, func):
        if func in self.input_calls:
            del self.input_calls[self.input_calls.index(func)]
