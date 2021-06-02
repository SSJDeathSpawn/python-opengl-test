#rendering/renderers/shapes.py

from ...basics.buffers import *
from OpenGL.GL import *
import numpy as np
from ...basics.shaders import *
from ...basics.vertex_array import *	
from ..rendering_registry import Renderer
from ...utils import *
import ctypes
import itertools
from collections import deque
from ...logger import Logger

logger = Logger('renderers/shapes')
#TODO: Fix Tree on top of player, play to see
class Shape(Renderer):
	def __init__(self):
		self.vao = VertexArray()
		self.vb = VertexBuffer()
		self.ib = IndexBuffer()
		self.pos_data = []
		self.col_data = []

	def define_shape(self, pos:np.ndarray, indices:np.ndarray, colours:np.ndarray):
		self.pos_data = pos
		self.col_data = colours
		vertex_data = np.array(np.append(self.pos_data, self.col_data, axis=1),dtype=np.float32).flatten()
		vl = VertexArrayLayout()
		vl.push(2, GL_FLOAT, False)
		vl.push(4, GL_FLOAT, False)
		self.vb.put_data(len(vertex_data) * 4, vertex_data)
		self.vao.set_layout(self.vb, vl)
		self.ib.put_data(ctypes.sizeof(GLuint)*len(indices), indices)

	def change_pos(self, offset):
		mod_pos_data = self.pos_data + offset
		vertex_data = np.array(np.append(mod_pos_data, self.col_data, axis=1),dtype=np.float32).flatten()
		self.vb.change_data(len(vertex_data) * ctypes.sizeof(GLfloat), vertex_data)

	def render(self, shader: ShaderProgram):
		#glLoadIdentity()
		self.vao.bind()
		shader.bind()
		self.ib.bind()
		glDrawElements(GL_TRIANGLES, self.ib.count, GL_UNSIGNED_INT, ctypes.c_void_p(0))
		self.ib.unbind()
		shader.unbind()
		self.vao.unbind()

class Polygon(Shape):
	def __init__(self, sides: int, pos: list, col:list):
		super().__init__()
		norm_pos = [arr2norm(*i) for i in pos]
		indices = self.triangulate(norm_pos.copy())
		col = [i for i in col] if np.array(col).ndim > 1 else [col]*sides
		self.define_shape(np.array(norm_pos, dtype=np.float32), np.array(indices, dtype=np.uintc), np.array(col, dtype=np.float32))

	#This one in particular had me needing to research 
	#Graphs I made in the process: 
	#https://www.desmos.com/calculator/g602w5htdj 
	#https://www.desmos.com/calculator/tii2fmsh97 (<-- isn't useful, had to use another way)
	#https://www.desmos.com/calculator/90kixqqskr
	#This generates the triangle index order with which the polygon should be rendered
	#Uses the ear method

	#Explanation of the method will be given in my project (hopefully).
	def triangulate(self, pos:list) -> list:
		pointer = 0
		indices = []
		length = len(pos)
		skip_list=[]
		while (len(pos) - len(skip_list)) > 2 :
			pointer_before = (pointer-1) % len(pos)  
			pointer_after = (pointer+1) % len(pos)
			while pointer_before in skip_list:
				pointer_before = (pointer_before - 1) % len(pos)
			while pointer_after in skip_list:
				pointer_after = (pointer_after + 1) % len(pos)
			x1,y1 = pos[pointer_before]
			x2,y2 = pos[pointer]
			x3,y3 = pos[pointer_after]
			twice_area = (x1 * (y2 - y3)) + (x2 * (y3 - y1)) + (x3 * (y1 - y2))
			#Collinear points
			if twice_area == 0:
				skip_list += [pointer]
				pointer = (pointer + 1) % len(pos)
			#Convex point
			elif twice_area < 0:
				for i in range(len(pos)):
					#Skip the triangle vertices
					d = deque(list(range(len(pos))))
					d.rotate(-pointer_before)
					rang = list(itertools.takewhile(lambda x: x!= pointer_after, d))
					rang.append(pointer_after)
					#Check if any other point is inside the current triangle
					if (i not in rang) and i not in skip_list:
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
							pointer = (pointer + 1) % len(pos)
							break
				#No points inside the triangle
				else:
					indices += [pointer_before, pointer, pointer_after]
					#Remove the ear
					skip_list += [pointer]
					pointer = (pointer + 1) % len(pos)
			#Skip if concave
			elif twice_area > 0:
					pointer = (pointer + 1) % len(pos)
			skip_list = list(set(skip_list))
			#logger.log_info(f"Indices = {indices}")
		for j in range(len(indices)):
				if indices[j] < 0:
						indices[j] = length + indices[j]
		return indices

#Used to draw multiple non-connected polygons onto the screen
#TODO: Make this batch render rather than individually draw call
class MultiplePolygons(Renderer):

	def __init__(self, count: int, **kwargs):
		self.polygons=[]
		for i in range(1, count+1):
			self.polygons.append(Polygon(kwargs['side' + str(i)], kwargs['pos' + str(i)], kwargs['col'+str(i)]))

	def render(self, shader: ShaderProgram):
		[i.render(shader) for i in self.polygons]

	def change_pos(self, offset):
		[i.change_pos(offset) for i in self.polygons]
