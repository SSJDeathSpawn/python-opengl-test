#basics/buffers.py

from OpenGL.GL import *
import numpy as np

#Used to give data to OpenGL
#This is gives data on all the points on the screen
class VertexBuffer(object):

	def __init__(self):
		self._id = glGenBuffers(1)

	def put_data(self, size: int, data: np.ndarray):
		glBindBuffer(GL_ARRAY_BUFFER, self._id)
		glBufferData(GL_ARRAY_BUFFER, size, data, GL_STATIC_DRAW)
		glBindBuffer(GL_ARRAY_BUFFER, 0)

	def bind(self):
		glBindBuffer(GL_ARRAY_BUFFER, self._id)

	def unbind(self):
		glBindBuffer(GL_ARRAY_BUFFER, 0)
	
	def __del__(self):
		glDeleteBuffers(1, self._id)

#Used to define the order in which the vertex positions should be drawn
#Since OpenGL can only render with triangles past like 3.0
#Lessens repition of data
class IndexBuffer(object):

	def __init__(self):
		self._id = glGenBuffers(1)

	def put_data(self, size: int, data:np.ndarray):
		self.count = len(data)
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._id)
		glBufferData(GL_ELEMENT_ARRAY_BUFFER, size, data, GL_STATIC_DRAW)
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

	def bind(self):
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._id)

	def unbind(self):
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
	
	def __del__(self):
		glDeleteBuffers(1, self._id)