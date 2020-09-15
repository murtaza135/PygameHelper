import pygame
from pygame.math import Vector2
from pygame_helper.rotator2 import Rotator2
from pygame_helper.positional_rect import PositionalRect
from pygame_helper.utilities import WHTuple, XYTuple, NESWTuple
from abc import ABC, abstractmethod


class AbstractMovementComponent(ABC):
    
    def __init__(self, parent, rect, default_position=(0, 0), default_rotation=0, window_size=(800, 600), should_wrap_screen=(True, True)):
        self.parent = parent
        self.rect = rect
        self.rect.center = (default_position[0], default_position[1])
        self.window_size = WHTuple(*window_size)

        self.position = PositionalRect(self.rect)
        self.velocity = Vector2()
        self.rotation = Rotator2(default_rotation)

        self.should_wrap_screen = XYTuple(*should_wrap_screen)

    @property
    def frametime(self):
        try:
            frametime_ms = self.parent.game_mode.game.clock.get_time()
        except AttributeError:
            frametime_ms = self.parent.game.clock.get_time()

        frametime_seconds = frametime_ms / 1000
        return frametime_seconds


    @abstractmethod
    def move(self):
        pass

    def move_with_collision(self, collide_fn_x, collide_fn_y, group, dokill=None, collide_callback=None):
        raise NotImplementedError


    def _wrap_around_screen_x(self):
        if self.position.centerx > self.window_size.width:
            self.position.centerx = 0
        elif self.position.centerx < 0:
            self.position.centerx = self.window_size.width

    def _wrap_around_screen_y(self):
        if self.position.centery > self.window_size.height:
            self.position.centery = 0
        elif self.position.centery < 0:
            self.position.centery = self.window_size.height