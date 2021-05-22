#rendering_registry.py

from abc import abstractmethod, ABC 
from typing import Type, Callable
from ..basics.shaders import *


class Renderer(ABC):
	
	@abstractmethod
	def render(self, shader: ShaderProgram) -> None:
		pass

class RenderRegistry(object):
	def __init__(self):
		#The list of acceptable renderers
		self._registered_renderers = []

	def add_renderer(self, renderer: Type[Renderer]) -> None:
		#Add a renderer to the list of acceptable renderers
		self._registered_renderers.append(renderer)

	#Check if the given renderer is in the list of acceptable renderers
	def is_valid_renderer(self, renderer):
		return type(renderer) in self._registered_renderers

	# def render_all(self, shader: ShaderProgram) -> None:
	# 	#Every acceptale renderer should render on screen with no exception (not optimal)
	# 	for renderer in self._registered_renderers:
	# 		renderer.render(shader) 

	# def render_selected(self, shader: ShaderProgram, predicate: Callable[[Type[Renderer]], bool]) -> None:
	# 	#Every render that return true when passed through the given function should render on screen
	# 	renderers = list(filter(predicate, self._registered_renderers))
	# 	for renderer in renderers:
	# 		renderer.render(shader)