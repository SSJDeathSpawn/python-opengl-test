#rendering/renders.py

from OpenGL.GL import *
from ..logger import *
from abc import ABC, abstractmethod
import yaml
import os


logger = Logger("Render Loader")

class BaseRenderLoader(ABC):

	@abstractmethod
	def get_renders(render_folder):
		pass

class MainRenderLoader(BaseRenderLoader):
	#recursively goes through a folder and gets all the yaml files
	def get_renders():
		render_folder = os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + '/../../res/renders')
		files = scandirs(render_folder, '.yaml')
		loaded_renders =[]
		for file in files:
			path = render_folder + '/' + file
			try:
				with open(path, mode='r') as f:
					temp = yaml.load(f, Loader=yaml.FullLoader)
					loaded_renders += [temp]
			except(FileNotFoundError):
				logger.log_warning(f"File ({file}) was deleted during program execution.")
		return loaded_renders
		
#Function for recursively going through a directory and getting all the files with a certain extension
def scandirs(path, ext:str) -> list:
	li = []
	for entry in os.scandir(path):
		if entry.is_dir():
			li+=scandirs(entry.path)
		if entry.is_file() and entry.path.endswith(ext):
			li.append(entry.name)
	return li
