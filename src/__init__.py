#__init__.py
from . import logger

logger = logger.Logger('Application Base')

should_exit = False

try:
	import OpenGL
	import OpenGL.GL
	import OpenGL.GLUT
	import OpenGL.GLU
except(ImportError):
	logger.log_error("You do not have the PyOpenGL library installed. Please install the module using 'pip install PyOpenGL PyOpenGL_accelerate'.")
	should_exit = True

try:
	import mysql.connector
except(ImportError):
	logger.log_error("You do not have the MySQL Connector library installed. Please install the module using 'pip install mysql-connector-python'.")
	should_exit = True

if should_exit:
	exit()

from . import application, logger, constants, basics, rendering

__all__ = ['logger', 'application', 'constants', 'basics', 'rendering']