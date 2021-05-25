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
from .rendering.renderers.shapes import *
import time
import os

from .logger import *
from OpenGL.GL import *


logger = Logger("Application Main")

class Application(object):

	internal_renderers = [
		Shape,
		Polygon,
		MultiplePolygons
	]

	# [ [function1, kwargs1],
	#	[function2, kwargs2] ]
	render_calls = []

	#Render whatever the game tells you to
	def render(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		[i[0](**i[1]) for i in self.render_calls]
		self.screen.swap_buffers()

	#Do stuff like initializing the screen and load all the available render files
	#All the game related stuff should be done in game.py
	def __init__(self):
		logger.log_info("Initialization step")
		start_time = time.time()
		self.render_handler = RenderHandler()
		[self.render_handler.register_renderer(i) for i in self.internal_renderers]
		self.render_handler.load_renders()
		self.screen = Screen("Project", (SCREEN_WIDTH, SCREEN_HEIGHT), self.render)
		self.render_handler.convert_renders()
		self.screen.clear(0,0.1,0.1,1)
		self.default_shader = self.compile_shaders()

	#Convenience function to get render_handler
	def get_render_handler(self):
		return self.render_handler

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
		glutMainLoop()
