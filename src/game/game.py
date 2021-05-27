#game.py
from ..application import Application 
from ..logger import Logger
from .scenes.scene import TestScene
logger = Logger("Game")

#Game layer of stuff, doesn't need to bother with backend stuff
#Backend is dealt by Application (application.py) 
class Game(object):
    def __init__(self):
        self.current_scene = None
        self.application = Application()
        self.load_scene(TestScene())
        self.application.add_tick_func(self.tick, {}) 
        self.application.run()

    def load_scene(self, scene):
        self.current_scene = scene
    
    def render(self, application, shader):
        self.current_scene.render_objects(self.application, self.application.default_shader)

    def tick(self):
        self.render(self.application, self.application.default_shader)
        self.current_scene.tick()
