#first.py

from OpenGL.GL import *
from OpenGL.GL.shaders import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from .constants import *
from .basics.buffers import *
from .basics.shaders import *
from .basics.vertex_array import *
from .basics.shapes import *
from .logger import *
import numpy as np
import ctypes
import time

logger = Logger("Application Main")

null = ctypes.c_void_p(0)
size_of_float = ctypes.sizeof(GLfloat)
actual_pos_1 = np.array([[46,  46],
						 [46, 233],
						 [336, 47],
						 [336, 233]
						], dtype=np.float32)

actual_pos_2 = np.array([ [210, 126],
						  [210, 317],
						  [524, 126],
						  [524, 317]
						], dtype=np.float32)

aspect_ratio = np.array([SCREEN_WIDTH, SCREEN_HEIGHT],dtype=np.float32)

actual_pos_1_norm = np.divide(actual_pos_1, (aspect_ratio/2))-1
actual_pos_2_norm = np.divide(actual_pos_2, (aspect_ratio/2))-1

colours_1 = np.array([[1.0,0.0,0.0,0.5]]*4)
colours_2 = np.array([[0.0,0.0,1.0,0.5]]*4)
indices = np.array([
	0, 1, 2,
	1, 2, 3
	], dtype=np.uint8)

def show_screen():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	rect1.render(program)
	rect2.render(program)
	glutSwapBuffers()

def init_values():
	logger.log_info("Defining shapes...")
	global rect1, rect2
	rect1 = Shape()
	rect2 = Shape()
	rect1.define_shape(actual_pos_1_norm, indices, colours_1)
	rect2.define_shape(actual_pos_2_norm, indices, colours_2)

def init_shader():
	logger.log_info("Compiling shaders...")
	vertex = Shader('../res/shaders/vertex.glsl', GL_VERTEX_SHADER)
	fragment = Shader('../res/shaders/fragment.glsl', GL_FRAGMENT_SHADER)
	vertex.compile()
	fragment.compile()
	
	global program
	program = ShaderProgram(vertex, fragment)
	program.compile()


def init_screen():
	logger.log_info("Initializing screen...")
	glutInitDisplayMode(GLUT_RGBA)
	glutInitWindowSize(SCREEN_WIDTH,SCREEN_HEIGHT)
	glutInitWindowPosition(100,100)
	global wind
	wind = glutCreateWindow("Test")
	glutDisplayFunc(show_screen)
	glutIdleFunc(show_screen)
	glClearColor(0,0.1,0.1,1)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	
def init():
	logger.log_info("Initialization step")
	start_time = time.time()
	glutInit()
	init_screen()
	init_values()
	init_shader()
	logger.log_info(f"Initialization took {time.time() - start_time} seconds")

def run():
	glutMainLoop()
