#basics/shapes.py

from ...basics.buffers import *
from OpenGL.GL import *
import numpy as np
from ...basics.shaders import *
from ...basics.vertex_array import *	
from ..rendering_registry import Renderer
from ...utils import *
import ctypes
from itertools import cycle
from ...logger import Logger

class Shape(Renderer):
	def __init__(self):
		self.vao = VertexArray()
		self.vb = VertexBuffer()
		self.ib = IndexBuffer()

	def define_shape(self, pos:np.ndarray, indices:np.ndarray, colours:np.ndarray):
		self.ib.put_data(ctypes.sizeof(GLubyte)*len(indices), indices)
		vertex_data = np.array(np.append(pos,colours, axis=1),dtype=np.float32).flatten()
		self.vb.put_data(len(vertex_data) * ctypes.sizeof(GLfloat), vertex_data)
		vl = VertexArrayLayout()
		vl.push(2, GL_FLOAT, False)
		vl.push(4, GL_FLOAT, False)
		self.vao.set_layout(self.vb, vl)

	def render(self, shader: ShaderProgram):
		glLoadIdentity()
		self.vao.bind()
		shader.bind()
		self.ib.bind()
		glDrawElements(GL_TRIANGLES, self.ib.count, GL_UNSIGNED_BYTE, ctypes.c_void_p(0))
		self.ib.unbind()
		shader.unbind()
		self.vao.unbind()

logger = Logger('shapes/Polygon')
class Polygon(Shape):
	def __init__(self, sides: int, pos: list, col:list):
		super().__init__()
		norm_pos = []
		for i in pos:
			norm_pos.append(arr2norm(*i))
		indices = self.triangulate(norm_pos.copy())
		self.define_shape(np.array(norm_pos, dtype=np.float32), np.array(indices, dtype=np.uint8), np.array(col, dtype=np.float32))

	#This one was hard. Actually used 11th grade (equivalent) Maths 
	#Graphs I made in the process: https://www.desmos.com/calculator/g602w5htdj 
	#https://www.desmos.com/calculator/tii2fmsh97 (<-- isn't useful, had to use another way)
	#https://www.desmos.com/calculator/90kixqqskr
	#This generates the triangle index order with which the polygon should be rendered
	#Uses the ear method

	def triangulate(self, pos:list) -> list:
		pointer = 1
		indices = []
		length = len(pos)
		skip_list=[]
		while (len(pos) - len(skip_list)) > 2 :
			pointer_before = pointer-1
			pointer_after = (pointer+1) % len(pos)
			while pointer_before in skip_list:
				if pointer_before < 0:
					pointer_before = len(pos)-1
				pointer_before -= 1
			while pointer_after in skip_list:
				if pointer_after > (len(pos)-1):
					pointer_after = 0
				pointer_after += 1
			x1,y1 = pos[pointer_before]
			x2,y2 = pos[pointer]
			x3,y3 = pos[pointer_after]
			twice_area = (x1 * (y2 - y3)) + (x2 * (y3 - y1)) + (x3 * (y1 - y2))
			#Collinear points
			if twice_area == 0:
				skip_list += [pointer]
				pointer += 1
			#Convex point
			elif twice_area < 0:
				for i in range(len(pos)):
					#Skip the triangle vertices
					if (i not in range(pointer_before, pointer_after+1)) and i not in skip_list:
						Px,Py = pos[i]
						#Altered Distance (Point to line) formula (after subbing a,b,c (ax+by+c) from point form of line)
						v1 = (x2 - x1) * (Py - y2) - (y2 - y1) * (Px - x2)
						v2 = (x3 - x2) * (Py - y3) - (y3 - y2) * (Px - x3)
						v3 = (x1 - x3) * (Py - y1) - (y1 - y3) * (Px - x1)
						#Will be found as collinear later
						if (v1 == 0 or v2 == 0 or v3 == 0):
							skip_list += [i]
						#There should be no points inside the triangle
						if(v1 < 0 and v2 < 0 and v3 < 0):
							pointer += 1
							break
				#No points inside the triangle
				else:
					indices += [pointer_before, pointer, pointer_after]
					#Remove the ear
					skip_list += [pointer]
					pointer += 1
			#Skip if concave
			elif twice_area > 0:
				pointer +=1
			skip_list = list(set(skip_list))
		for j in range(len(indices)):
			if indices[j] < 0:
				indices[j] = length + indices[j]
		return indices