#basics/shaders.py

from OpenGL.GL.shaders import *
from OpenGL.GL import *
from ..logger import *
import os


logger = Logger("Application Shader")

class ShaderProgram(object):
	def __init__(self, vertex, fragment):
		self.vertex = vertex
		self.fragment = fragment

	def compile(self):
		self.id = compileProgram(self.vertex._id, self.fragment._id)

	def bind(self):
		glUseProgram(self.id)

	def unbind(self):
		glUseProgram(self.id)

class Shader(object):
	#Goes to the file with the given path and copies it to self.raw_code
	def __init__(self, path, type:GLenum):
		self._path = ''
		self.type = type
		if path.startswith('./') or path.startswith('../') or path.startswith('/./') or path.startswith('/../'):
			self._path = os.path.dirname(os.path.realpath(__file__)) + "/.." + (path if path[0] == '/' else '/' + path)
		self.raw_code = ''
		try:
			with open(self._path,'rt') as f:
				self.raw_code = f.read().strip()
		except(IOError):
			logger.log_warning("File does not exist or is not usable at the moment.")

	#using self.raw_code, compile the shader
	def compile(self):
		self._id = compileShader(self.raw_code, self.type)