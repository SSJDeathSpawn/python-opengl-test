#basics/window.py

from OpenGL.GLUT import *
from OpenGL.GL import *
from typing import Callable, Tuple, List

class Screen(object):

	xy_tuple = Tuple[int, int]

	def __init__(self, title:str, size: xy_tuple, render_function:Callable, window_position: xy_tuple = (100, 100)) -> None:
		glutInit()
		glutInitDisplayMode(GLUT_RGBA)
		glutInitWindowSize(size[0], size[1])
		glutInitWindowPosition(window_position[0], window_position[1])
		self.wind = glutCreateWindow(title)
		glutDisplayFunc(render_function)
		glutIdleFunc(render_function)
		self.clear(0,0,0,0)
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

	def clear(self, r, g, b, a):
		glClearColor(r,g,b,a)

	def swap_buffers(self):
		glutSwapBuffers()