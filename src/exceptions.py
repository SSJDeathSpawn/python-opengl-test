#exceptions.py
from .logger import Logger


logger = Logger("Exception")

#The exception raised when loading from a renderer that is not registered in the rendering registry
class InvalidRendererException(Exception):
	default_message = '{name} is not a valid renderer. It is not registered with the rendering registry!'
	def __init__(self, renderer, message = default_message) -> None:
		logger.log_error(default_message.format(name=str(renderer)))
