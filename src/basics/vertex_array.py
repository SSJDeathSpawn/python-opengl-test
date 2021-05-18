#basics/vertex_array.py
from .buffers import *
from OpenGL.GL import *
import ctypes


def get_size_from_type(type):
	return_dict = {
	GL_FLOAT: ctypes.sizeof(GLfloat),
	GL_UNSIGNED_INT: ctypes.sizeof(GLuint),
	GL_UNSIGNED_BYTE: ctypes.sizeof(GLubyte)
	}
	return return_dict[type]

class VertexArrayLayout(object):
	def __init__(self):
		self.elements = []
		self.stride = 0

	def push(self, count, type, normalized):
		self.elements.append((type, count, normalized))
		self.stride += count * get_size_from_type(type)

	def get_elements(self):
		return self.elements.copy()

class VertexArray(object):
	def __init__(self):
		self._id = glGenVertexArrays(1)

	def set_layout(self, vb: VertexBuffer, vl: VertexArrayLayout):
		self.bind()
		vb.bind()
		elements = vl.get_elements()
		offset = 0
		for i in range(len(elements)):
			element = elements[i]
			glEnableVertexAttribArray(i)
			glVertexAttribPointer(i, element[1], element[0], element[2], vl.stride, ctypes.c_void_p(offset))
			offset += element[1] * get_size_from_type(element[0])
		vb.unbind()
		self.unbind()

	def bind(self):
		glBindVertexArray(self._id)

	def unbind(self):
		glBindVertexArray(0)