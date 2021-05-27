#game/scenes/scene.py
from ..objects.game_object import GameObject
from ..objects.player import Player
from ...logger import Logger
import math

logger = Logger("game/scenes/scene")
class ObjectInScene():
    def __init__(self, obj, pos=[0,0]):
        #GL Coords. Not pixel coords
        self.pos=pos
        self.obj = obj
        self.is_rendered = False
        self.render_id = ""

    def render(self, application, shader):
        self.render_id = self.obj.render(application, shader, self.pos)
        self.is_rendered = True

    def stop_rendering(self, application):
        if self.is_rendered:
            self.obj.stop_rendering(application, self.render_id)

class Scene(object):
    def __init__(self):
        self.objects = {}
    
    def add_object(self, name, obj):
        if isinstance(obj, ObjectInScene):
           self.objects[name] = obj
        elif isinstance(obj, GameObject):
            self.objects[name] = ObjectInScene(obj)
        else:
            raise TypeError(f"{str(obj)} is not a valid instance of GameObject or ObjectInScene ")

    def render_objects(self, application, shader, predicate=lambda _: True):
        for i in self.objects:
            if predicate(self.objects[i]):
                self.objects[i].render(application, shader)

    def remove_render_calls(self, application):
        for i in self.objects:
            self.objects[i].stop_rendering(application)
    
    def tick(self):
        pass

class TestScene(Scene):
    def __init__(self):
        super().__init__()
        self.player = ObjectInScene(Player())
        self.theta = 0
        self.add_object('Player', self.player)
        self.objects['Player'].pos=[-0.5,0]

    def tick(self):
        r = 0.2
        self.objects['Player'].pos = [r * math.cos(self.theta), r * math.sin(self.theta)]
        self.theta += 0.01
