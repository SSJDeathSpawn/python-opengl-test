#application.py

from OpenGL.GL import *
from OpenGL.GL.shaders import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from .basics.window import *
from .constants import *
from .rendering.rendering_registry import RenderRegistry
from .rendering.rendering_handler import RenderHandler
from .basics.shaders import ShaderProgram, Shader
import time
import os

from .logger import *
from OpenGL.GL import *


logger = Logger("Application Main")

class Application(object):

	def render(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		self.render_handler.render('Basic Rectangle', self.shader_program)
		self.screen.swap_buffers()

	def __init__(self):
		logger.log_info("Initialization step")
		start_time = time.time()
		self.render_handler = RenderHandler()
		self.render_handler.load_renders()
		self.screen = Screen("Project", (SCREEN_WIDTH, SCREEN_HEIGHT), self.render)
		self.render_handler.convert_renders()
		self.screen.clear(0,0.1,0.1,1)
		self.shader_program = self.compile_shaders()
		self.run()

	def get_render_handler(self):
		return self.render_handler

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
		glutMainLoop()
