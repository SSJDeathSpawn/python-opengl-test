#basics/buffers.py

from OpenGL.GL import *
import numpy as np

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