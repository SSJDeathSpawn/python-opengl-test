#exceptions.py
from .logger import Logger


logger = Logger("Exception")
class InvalidRendererException(Exception):
	default_message = '{name} is not a valid renderer. It is not registered with the rendering registry!'
	def __init__(self, renderer, message = default_message) -> None:
		logger.log_info(default_message.format(name=str(renderer)))
