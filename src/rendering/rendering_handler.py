#rendering/rendering_handler.py
from .renders import BaseRenderLoader
from importlib import import_module
from ..logger import *
from .renderers import shapes
from .rendering_registry import Renderer, RenderRegistry
from ..basics.shaders import ShaderProgram
from .renders import BaseRenderLoader, MainRenderLoader
from ..exceptions import InvalidRendererException
from typing import Type
from ..utils import random_id

logger = Logger("Rendering Handler")
class RenderHandler(object):
    def __init__(self):
        self.rendering_registry = RenderRegistry()
        self.loaded_renders = []
        self.converted_renders = {}

    def register_renderer(self, renderer:Type[Renderer]):
        self.rendering_registry.add_renderer(renderer)

    def load_renders(self, *render_loaders: Type[BaseRenderLoader]):
        #Get base render files
        self.loaded_renders.extend(MainRenderLoader.get_renders())
        #Get custom render files
        for i in render_loaders:
            if issubclass(i, BaseRenderLoader):
                self.loaded_renders.extend(i.get_renders())

    def convert_renders(self, *modules: str):
        module_dict = {}

        #Examples (and internal, acceptable bases)
        module_dict['shapes/Polygon'.lower()] = shapes.Polygon
        module_dict['shapes/Shape'.lower()] = shapes.Shape
        module_dict['shapes/MultiplePolygons'.lower()] = shapes.MultiplePolygons
        #Iterate through every custom 'base' value and add it to list of acceptable bases
        for module in modules:
            path, submodule = '.renderers.' + ".".join(module.split(sep = '/')[:-1]), module.split(sep='/')[-1]
            try:
                mod = import_module(path)
                submod = getattr(mod, submodule)
            except(ImportError, AttributeError):
                logger.log_warning(f"Had trouble import module {module}")
            else:
                if(issubclass(submod, Renderer)):
                    module_dict[module.lower()] = submod
                else:
                    logger.log_warning(f"{submod.__name__} is not an instance of Renderer. Skipping...")
        #Turning 'base' strings into concrete instances of Renderer classes
        for render in self.loaded_renders: 
            if render['base'] in module_dict:
                self.converted_renders[render['name']] = module_dict[render['base']](**render['info'])
            else:
                logger.log_warning(f"Render {render['name']} has an invalid base {render['base']}")

    def render(self, name: str, shader:ShaderProgram, pos=[0,0]) -> str:
        try:
            #logger.log_info(self.rendering_registry.is_valid_renderer(self.converted_renders[name]))
            if(self.rendering_registry.is_valid_renderer(self.converted_renders[name])):
                self.converted_renders[name].change_pos(pos)
                self.converted_renders[name].render(shader)
            else:
                raise InvalidRendererException(self.converted_renders['name'])
        except(KeyError):
            logger.log_warning(f"Render {name} not found")
