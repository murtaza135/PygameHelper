import pygame
from abc import ABC, abstractmethod
import collections
from pygame_helper import exceptions


class Widget(ABC):

    def __init__(self, action=None):
        if not pygame.display.get_init():
            raise exceptions.PygameInitError

        super().__init__()
        self.action = None
        self.set_action(action)
    
    def set_action(self, fn):
        if fn is not None and not isinstance(fn, collections.Callable):
            raise TypeError("Must provide a function")
        
        self.action = fn

    def get_centre_position_for_widget(self, initial_position, widget_geometry):
        widget_geometry_halved = (widget_geometry[0]/2, widget_geometry[1]/2)
        final_position = (initial_position[0] - widget_geometry_halved[0], initial_position[1] - widget_geometry_halved[1])
        return final_position

    @abstractmethod
    def render(self, window, position):
        pass