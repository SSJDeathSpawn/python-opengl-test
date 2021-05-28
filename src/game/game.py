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
        self.application.run()

    def load_scene(self, scene):
        if self.current_scene:
            self.application.remove_tick_func(self.current_scene.tick)
            self.application.input_handler.unsubscribe(self.current_scene.handle_input)
        self.current_scene = scene
        self.application.add_tick_func(self.current_scene.tick, {'application': self.application, 'shader': self.application.default_shader}) 
        self.application.input_handler.subscribe(self.current_scene.handle_input)
