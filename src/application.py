#application.py

from OpenGL.GL import *
from OpenGL.GL.shaders import *
from glfw import *
from OpenGL.GLU import *
from .basics.window import *
from .constants import *
from .rendering.rendering_registry import RenderRegistry
from .rendering.rendering_handler import RenderHandler
from .basics.shaders import ShaderProgram, Shader
from .rendering.renderers.shapes import *
from .input.input_handler import InputHandler
from .camera import Camera
import time
import os

from .logger import *
from OpenGL.GL import *


logger = Logger("Application Main")
#TODO: Make orthographic projection matrix which can move
class Application(object):

    internal_renderers = [
        Shape,
        Polygon,
        MultiplePolygons
    ]

    # [ [function1, kwargs1],
    #	[function2, kwargs2] ]
    render_calls = []
    tick_funcs = []

    #Render whatever the game tells you to
    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        [i[0](**i[1]) for i in self.tick_funcs]
        [i[0](**i[1]) for i in self.render_calls]
        self.default_shader.send_uniform_data("proj_mat", self.camera.proj_mat)
        self.render_calls = []

    #Do stuff like initializing the screen and load all the available render files
    #All the game related stuff should be done in game.py
    def __init__(self):
        start_time = time.time()
        logger.log_info("Initialization step")
        self.render_handler = RenderHandler()
        self.input_handler = InputHandler()
        [self.render_handler.register_renderer(i) for i in self.internal_renderers]
        self.render_handler.load_renders()
        self.screen = Screen("Project", (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.camera = Camera()
        self.screen.set_input_handler(self.input_handler)
        self.render_handler.convert_renders()
        self.screen.clear(0,0.1,0.1,1)
        self.default_shader = self.compile_shaders()
        logger.log_info(f"Initialization took {time.time() - start_time} seconds.")

    #Convenience function to get render_handler
    def get_render_handler(self):
        return self.render_handler
    
    def add_render_call(self, func, arguments):
        self.render_calls.append([func, arguments])

    def add_tick_func(self, func, arguments):
        self.tick_funcs.append([func, arguments])

    def remove_tick_func(self, func):
        if func in [i[0] for i in self.tick_funcs]:
            del self.tick_funcs[[i[0] for i in self.tick_funcs].index(func)]
        
    #TODO: Accpet vertex and fragment shaders as arguments
    def compile_shaders(self):
        logger.log_info("Compiling shaders...")
        vertex = Shader('../res/shaders/vertex.glsl', GL_VERTEX_SHADER)
        fragment = Shader('../res/shaders/fragment.glsl', GL_FRAGMENT_SHADER)
        vertex.compile()
        fragment.compile()
        program = ShaderProgram(vertex, fragment)
        program.compile()
        return program

    def run(self):
        self.screen.main_loop(self.render)
