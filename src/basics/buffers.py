#basics/buffers.py

from OpenGL.GL import *
import numpy as np
import ctypes
from ..logger import Logger

#Used to give data to OpenGL
#This is gives data on all the points on the screen
logger = Logger("basics/buffers")
class VertexBuffer(object):

    def __init__(self):
        self._id = glGenBuffers(1)

    def put_data(self, size: int, data: np.ndarray):
        self.bind()
        glBufferData(GL_ARRAY_BUFFER, size, data, GL_DYNAMIC_DRAW)
        self.unbind()

    def change_data(self, size: int, data: np.ndarray):
        self.bind()
        glBufferSubData(GL_ARRAY_BUFFER, (0), size, data)
        self.unbind()

    def get_data(self, size: int):
        self.bind()
        data = np.array([])
        glGetBufferSubData(GL_ARRAY_BUFFER, 0, size, data)
        self.unbind()
        return data

    def bind(self):
        glBindBuffer(GL_ARRAY_BUFFER, self._id)

    def unbind(self):
        glBindBuffer(GL_ARRAY_BUFFER, 0)

#Used to define the order in which the vertex positions should be drawn
#Since OpenGL can only render with triangles past like 3.0
#Lessens repetition of data
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
    
