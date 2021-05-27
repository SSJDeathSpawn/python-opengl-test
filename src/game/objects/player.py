#game/objects/player.py
from .game_object import GameObject

class Player(GameObject):
    def __init__(self):
        pass

    def display(self, application, shader, pos):
        application.get_render_handler().render('Starting Player', shader, pos)
   
    def render(self, application, shader, pos):
        application.add_render_call(self.display, {'application':application, 'shader':shader, 'pos': pos})

        
