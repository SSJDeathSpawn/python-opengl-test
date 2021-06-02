#game/objects/tree.py
from ...logger import Logger
from .game_object import GameObject

logger = Logger('game/objects/Tree')
class Tree(GameObject):
	
	def __init__(self, pos=[0,0]):
		super().__init__(pos)

	def display(self, application, shader):
		application.get_render_handler().render('Tree', shader, self.pos)

	def render(self, application, shader):
		application.add_render_call(self.display, {'application': application, 'shader': shader})

	def tick(self, application, shader):
		if application.camera.should_be_rendered(self.pos):
			self.render(application, shader)