#game.py
from ..application import Application 
from ..logger import Logger

logger = Logger("Game")

#Game layer of stuff, doesn't need to bother with backend stuff
#Backend is dealt by Application (application.py) 
class Game(object):
	def __init__(self):
		self.application = Application()
		self.application.render_calls.append([self.test_scene, {'name':'Starting Player', 'shader':self.application.default_shader}])
		self.application.run()

	def test_scene(self, name, shader):
		self.application.get_render_handler().render(name, shader)

