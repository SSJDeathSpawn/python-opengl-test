#basics/window.py
import glfw
from OpenGL.GL import *
from typing import Callable, Tuple, List
from ..logger import Logger

logger = Logger("Application Window")
#Uses GLFW to initialize a window and sets the OpenGL context to that window
class Screen(object):

    xy_tuple = Tuple[int, int]

    def __init__(self, title:str, size: xy_tuple, window_position: xy_tuple = (100, 100)) -> None:
        if not glfw.init():
            logger.log_error("GLFW could not initialize")
            quit()
        self.wind = glfw.create_window(size[0], size[1], title, None, None)
        if not self.wind:
            logger.log_error("GLFW Window could not be created")
            glfw.terminate()
            quit()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        #This is the line that sets the context
        glfw.make_context_current(self.wind)
        glfw.swap_interval(1)
        self.clear(0,0,0,0)
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        glOrtho(-1, 1, -1, 1, -1.25, 1.25);
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL);
        glEnable(GL_BLEND)
        glAlphaFunc(GL_GREATER, 0.9);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def main_loop(self, render_function:Callable):
        while not glfw.window_should_close(self.wind):
            render_function()
            glfw.swap_buffers(self.wind)
            glfw.poll_events()
        glfw.terminate()


    def clear(self, r, g, b, a):
        glClearColor(r,g,b,a)
    
    def set_input_handler(self, input_handler):
        glfw.set_key_callback(self.wind, input_handler.handle_input)
