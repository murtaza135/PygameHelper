import pygame
from pygame.math import Vector2
from pygame_helper.rotator2 import Rotator2
from pygame_helper.positional_rect import PositionalRect
from pygame_helper.utilities import WHTuple, XYTuple, NESWTuple
from abc import ABC, abstractmethod


class AbstractMovementComponent(ABC):

    ### movement_type ###
    FOUR_WAY_MOVEMENT = "four_way_movement"
    EIGHT_WAY_MOVEMENT = "eight_way_movement"
    ROTATIONAL_MOVEMENT = "rotational_movement"

    ### direction_control ###
    DIRECTION_ONLY = "direction_only"
    DIRECTION_AND_MAGNITUDE = "direction_and_magnitude"

    
    def __init__(self, game_mode, parent_sprite, rect, movement_type, direction_control, direction_control_y=None,
                default_position=(0, 0), default_rotation=0, window_size=(800, 600), should_wrap_screen=(True, True)):
        self.game_mode = game_mode
        self.parent_sprite = parent_sprite
        self.rect = rect
        self.rect.center = (default_position[0], default_position[1])
        self.window_size = WHTuple(*window_size)

        self.position = PositionalRect(self.rect)
        self.velocity = Vector2()
        self.rotation = Rotator2(default_rotation)

        self.movement_type = movement_type
        self.direction_control = direction_control
        self.direction_control_y = direction_control_y

        self.should_wrap_screen = XYTuple(*should_wrap_screen)

        self._check_direction_control_y_for_eight_way_movement()

    @property
    def frametime(self):
        try:
            frametime_ms = self.game_mode.game.clock.get_time()
        except AttributeError:
            frametime_ms = self.game_mode.clock.get_time()
        frametime_seconds = frametime_ms / 1000
        return frametime_seconds

    def _check_direction_control_y_for_eight_way_movement(self):
        if self.movement_type == AbstractMovementComponent.EIGHT_WAY_MOVEMENT:
            if self.direction_control_y is None:
                raise ValueError("direction_control_y cannot be None if Eight Way Movement is used")


    ### Movement Section: Sets physics states & transforms depending upon input and collisions ###
    @abstractmethod
    def move(self):
        pass

    def move_with_collision(self, collide_fn_x, collide_fn_y, group, dokill=None, collide_callback=None):
        raise NotImplementedError

    def wrap_around_screen_x(self):
        if self.position.centerx > self.window_size.width:
            self.position.centerx = 0
        elif self.position.centerx < 0:
            self.position.centerx = self.window_size.width

    def wrap_around_screen_y(self):
        if self.position.centery > self.window_size.height:
            self.position.centery = 0
        elif self.position.centery < 0:
            self.position.centery = self.window_size.height


    ### Input Section: change acceleration, velocity and/or rotation DIRECTLY from input ###
    @abstractmethod
    def _process_movement_input(self):
        pass

    
    ### Collision Section: Only DETECTS collision, no movement occurs ###
    @abstractmethod
    def get_x_collision(self, group):
        pass

    @abstractmethod
    def get_collision_right(self, group):
        pass

    @abstractmethod
    def get_collision_left(self, group):
        pass

    @abstractmethod
    def get_y_collision(self, group):
        pass

    @abstractmethod
    def get_collision_bottom(self, group):
        pass

    @abstractmethod
    def get_collision_top(self, group):
        pass

    @staticmethod
    def collide_positional_rect(sprite_one, sprite_two):
        return sprite_one.movement.position.rect.colliderect(sprite_two.rect)

    @staticmethod
    def collide_positional_rect_if_possible(sprite_one, sprite_two):
        try:
            return sprite_one.movement.position.rect.colliderect(sprite_two.rect)
        except AttributeError:
            return sprite_one.rect.colliderect(sprite_two.rect)