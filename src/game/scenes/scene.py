#game/scenes/scene.py
from ..objects.game_object import GameObject
from ..objects.player import Player
from ..objects.tree import Tree
from ...logger import Logger
import math
import random
import numpy as np

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
    def __init__(self, tree_seed):
        super().__init__()
        self.player = Player()
        self.add_object('Player', self.player)
        self.generate_trees(start_pos=-10, end_pos=10, spread=1, disp_rand=0.5, seed=tree_seed)

    def tick(self, application, shader):
        [self.objects[i].tick(application, shader) for i in self.objects] 

    def handle_input(self, window, key, scancode, action, mods):
        [self.objects[i].handle_input(window, key, scancode, action, mods) for i in self.objects]

    def generate_trees(self, start_pos, end_pos, spread, disp_rand, seed):
        init_locs = [np.array([x, y]) for x in np.arange(start_pos,end_pos,spread) for y in np.arange(start_pos,end_pos,spread)]
        final_locs = []
        #Set seed
        random.seed(seed)
        #Displace the tree by a random amount
        for i in init_locs:
            disp = np.array([random.random() * disp_rand, random.random() * disp_rand])
            final_locs.append(i + disp)
        #Place the trees in their respective locations
        for i in range(len(final_locs)):
            tree = Tree(pos=final_locs[i])
            self.add_object('Tree' + str(i+1), tree)

