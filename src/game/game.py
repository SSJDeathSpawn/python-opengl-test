#game.py
from ..application import Application 
from ..logger import Logger
from .scenes.scene import TestScene
import time
logger = Logger("Game")

#Game layer of stuff, doesn't need to bother with backend stuff
#Backend is dealt by Application (application.py) 
class Game(object):
    def __init__(self):
        self.current_scene = None
        self.application = Application()
        start_time = time.time()
        logger.log_info("Loading Scene")
        self.load_scene(TestScene(5))
        logger.log_info(f"Loading took {time.time() - start_time} seconds.")
        self.application.run()

    def load_scene(self, scene):
        if self.current_scene:
            self.application.remove_tick_func(self.current_scene.tick)
            self.application.input_handler.unsubscribe(self.current_scene.handle_input)
        self.current_scene = scene
        self.application.add_tick_func(self.current_scene.tick, {'application': self.application, 'shader': self.application.default_shader}) 
        self.application.input_handler.subscribe(self.current_scene.handle_input)
