#game/objects/object.py


class GameObject(object):
    def __init__(self, pos=[0,0]):
        #GL Coords. Not pixel coords
        self.pos = pos
        self.is_rendered = False
    
    def handle_input(self, window, key, scancode, action, mods):
        pass

    def render(self, application, shader):
        pass
    
    def tick(self, application, shader):
        pass
