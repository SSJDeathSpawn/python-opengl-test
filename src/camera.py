#camera.py
import numpy as np
from .logger import Logger

logger = Logger("Camera")
#I guess there is a lot of maths related things here
class Camera(object):
	def __init__(self, left = -1, right = 1, up = 1, down=-1):
		#Will be taught in future, can't wait to find out how school teaches/ruins this for me
		mid_x = (left + right) / 2
		mid_y = (down + up) / 2
		#Who needs an Z axis in a 2D game?
		#Projection matrix
		self.proj_mat = np.array([[1,0,0,-mid_x], [0,1,0,-mid_y], [0,0,1,-mid_y], [0,0,0,1]])

	def move_to_pos(self, pos):
		self.proj_mat = np.array([[1, 0, 0, -pos[0]],[0, 1, 0, -pos[1]],[0, 0, 1, -pos[1]],[0, 0, 0, 1]])

	def offset_cam(self, offset):
		self.proj_mat = np.array([[1,0,0,offset[0]], [0,1,0,offset[1]], [0,0,1,offset[1]], [0,0,0,1]]) @ self.proj_mat 
		logger.log_info(self.proj_mat)

	def zoom(self, scale):
		self.proj_mat = self.proj_mat @ np.array([[scale, 0, 0, 0], [0, scale, 0, 0], [0, 0, 0, 0],[0, 0, 0, 1]])

	def should_be_rendered(self, pos):
		screen_pos = (self.proj_mat @ np.array([[pos[0]], [pos[1]], [0], [1]])).reshape(4)
		#Return if any of the objects are out of the 1.25 bounds of the viewable screen
		return all((i > -1.5 and i < 1.5) for i in screen_pos[:2])