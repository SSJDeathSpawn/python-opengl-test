#game/scenes/scene.py
from ..objects.game_object import GameObject
from ..objects.player import Player
from ...logger import Logger
import math

logger = Logger("game/scenes/scene")
class Scene(object):
    def __init__(self):
        self.objects = {}
    
    def add_object(self, name, obj):
        if isinstance(obj, GameObject):
            self.objects[name] = obj
        else:
            logger.log_error(f"{str(obj)} is not a valid instance of GameObject")
            raise TypeError()

    def render_objects(self, application, shader, predicate=lambda _: True):
        for i in self.objects:
            if predicate(self.objects[i]):
                self.objects[i].render(application, shader)

    def tick(self):
        pass

    def handle_input(self, window, key, scancode, action, mods):
        pass

class TestScene(Scene):
    def __init__(self):
        super().__init__()
        self.player = Player()
        self.theta = 0
        self.add_object('Player', self.player)
        self.objects['Player'].pos=[-0.5,0]

    def tick(self, application, shader):
        [self.objects[i].tick(application, shader) for i in self.objects] 

    def handle_input(self, window, key, scancode, action, mods):
        [self.objects[i].handle_input(window, key, scancode, action, mods) for i in self.objects]

