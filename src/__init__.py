#__init__.py
from . import logger

logger = logger.Logger('Application Base')

should_exit = False

try:
    import OpenGL
    import OpenGL.GL
    import OpenGL.GLU
    import mysql.connector
    import yaml
    import glfw
    import numpy
except(ImportError):
    logger.log_error("You do not have the required modules installed. Please install the module using 'pip install -r requirements.txt'.")
    should_exit = True

if should_exit:
    logger.log_info("If 'pip install ...' does not work, try 'python -m pip install ...'")
    exit()

from . import application, logger, constants, basics, rendering, game

__all__ = ['logger', 'application', 'constants', 'basics', 'rendering', 'game']
