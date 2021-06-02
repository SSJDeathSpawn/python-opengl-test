#game/objects/player.py
from .game_object import GameObject
from ...logger import Logger
import glfw
import numpy as np

logger = Logger("objects/player")
class Player(GameObject):
    def __init__(self, pos=[0,0]):
        super().__init__(pos)
        self.mov_speed = 0.01

    def display(self, application, shader):
        application.get_render_handler().render('Starting Player', shader, self.pos)
   
    def render(self, application, shader):
        application.add_render_call(self.display, {'application':application, 'shader':shader})
    
    def tick(self, application, shader):
        keys = application.input_handler.keys.copy()
        ver = int(keys[glfw.KEY_W]) + -int(keys[glfw.KEY_S])
        hor = int(keys[glfw.KEY_D]) + -int(keys[glfw.KEY_A])
        if ver != 0 or hor != 0:
            inp = np.array([hor, ver], dtype=np.float32)
            norm_inp = inp/(np.linalg.norm(inp)) #You thought you could get extra speed from holding both a vertical and horizontal key, didn't you?
            mov = norm_inp * self.mov_speed
            self.pos = list(mov+self.pos)
        application.camera.move_to_pos(self.pos)
        if application.camera.should_be_rendered(self.pos):
            self.render(application, shader)
