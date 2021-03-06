#utils.py
from .constants import *
from typing import List
import string
import random

generated_ids = []
#Convert pixel array values into OpenGL normalized values
def arr2norm(x:int,y:int) -> List[float]:
	actual_y = SCREEN_HEIGHT - y
	norm_x = x / (SCREEN_WIDTH/2) - 1 
	norm_y = actual_y / (SCREEN_HEIGHT/2) - 1
	return [norm_x, norm_y]

def random_id():
    temp = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(7)])
    while temp in generated_ids:
        temp = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(7)])
    generated_ids.append(temp)
    return temp
