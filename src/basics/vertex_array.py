#basics/vertex_array.py
from .buffers import *
from OpenGL.GL import *
from ..logger import Logger
import ctypes

logger = Logger("basics/vertex_array")
#get size (in bytes) from the GL equivalent
def get_size_from_type(type):
	return_dict = {
	GL_FLOAT: ctypes.sizeof(GLfloat),
	GL_UNSIGNED_INT: ctypes.sizeof(GLuint),
	GL_UNSIGNED_BYTE: ctypes.sizeof(GLubyte)
	}
	return return_dict[type]

#Used to define interleaved data for the vertex array (not really made for tightly packed data).
# PCT PCT PCT, not PPP CCC TTT
class VertexArrayLayout(object):
    def __init__(self):
        self.elements = []
        self.stride = 0

    def push(self, count, type, normalized):
        self.elements.append((type, count, normalized))
        self.stride += count * get_size_from_type(type)

    def get_elements(self):
        return self.elements.copy()

#Stores the data that is provided to Vertex Buffer. Can be used to instantly load and offload data. 
#Easier than loading into Vertex Buffer whenever an object is required to be drawn
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
            #The command that copies vertex buffer data into vertex array object
            glVertexAttribPointer(i, element[1], element[0], element[2], vl.stride, ctypes.c_void_p(offset))
            offset += element[1] * get_size_from_type(element[0])
        vb.unbind()
        self.unbind()

    def bind(self):
        glBindVertexArray(self._id)

    def unbind(self):
        glBindVertexArray(0)
