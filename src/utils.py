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

def coor2norm(co:float, rev:bool, max_size:int) -> float:
	norm_co = (max_size - co if rev else co) / max_size - 1
	return norm_co