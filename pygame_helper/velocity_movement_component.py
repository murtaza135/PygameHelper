import pygame
from pygame.math import Vector2
from rotator2 import Rotator2
from positional_rect import PositionalRect
from keybinder import Keybinder
from movement_component import MovementComponent
from utilities import WHTuple, XYTuple, NESWTuple
import math
from velocity_input_component import VelocityInputComponent
from velocity_collision_component import VelocityCollisionComponent


class VelocityMovementComponent(MovementComponent):
    
    def __init__(self, parent, rect, constant_velocity_delta, default_position=(0, 0), 
                default_velocity_delta=(0, 0), default_rotation=0, window_size=(800, 600), should_bounce=(False, False, False, False),
                should_wrap_screen=(True, True), movement_type="eight_way_movement",
                direction_control="direction_and_magnitude", direction_control_y=None):
        self.parent = parent
        self.rect = rect
        self.rect.center = (default_position[0], default_position[1])
        self.window_size = WHTuple(*window_size)

        self.position = PositionalRect(self.rect)
        self.velocity = Vector2()
        self.constant_velocity_delta = Vector2(constant_velocity_delta)
        self.default_velocity_delta = Vector2(default_velocity_delta)
        self.rotation = Rotator2(default_rotation)

        self.should_bounce = NESWTuple(*should_bounce)
        self.should_wrap_screen = XYTuple(*should_wrap_screen)

        self._keybinder = Keybinder("right", "left", "down", "up")
        self._movement_input = VelocityInputComponent(self, self._keybinder, movement_type, direction_control, direction_control_y)
        self._collision = VelocityCollisionComponent(self)

    @property
    def keybinds(self):
        return self._keybinder

    @property
    def movement_input(self):
        return self._movement_input

    @property
    def collision(self):
        return self._collision

    @property
    def frametime(self):
        frametime_ms = self.parent.game_mode.game.clock.get_time()
        frametime_seconds = frametime_ms / 1000
        return frametime_seconds


    def move(self):
        self._reset_velocity()
        self._movement_input.process_movement_input()
        self._set_new_physics_state_and_transform_x()
        self._set_new_physics_state_and_transform_y()

    def move_with_collision(self, collide_fn_x, collide_fn_y, group, dokill=None, collide_callback=None):
        self._reset_velocity()
        self._movement_input.process_movement_input()
        self._move_x_with_collision(collide_fn_x, group, dokill, collide_callback)
        self._move_y_with_collision(collide_fn_y, group, dokill, collide_callback)

    def _move_x_with_collision(self, collide_fn, group, dokill=None, collide_callback=None):
        self._set_new_physics_state_and_transform_x()

        sprite_collided = None
        if collide_fn is not None:
            sprite_collided = collide_fn(group, dokill, collide_callback)

        if sprite_collided is not None:
            self._move_x_back_if_collided(sprite_collided)
            self._apply_bounce_x(sprite_collided)

    def _move_y_with_collision(self, collide_fn, group, dokill=None, collide_callback=None):
        self._set_new_physics_state_and_transform_y()

        sprite_collided = None
        if collide_fn is not None:
            sprite_collided = collide_fn(group, dokill, collide_callback)

        if sprite_collided is not None:
            self._move_y_back_if_collided(sprite_collided)
            self._apply_bounce_y(sprite_collided)


    def _reset_velocity(self):
        self.velocity.x = self.constant_velocity_delta.x
        self.velocity.y = self.constant_velocity_delta.y

    def _set_new_physics_state_and_transform_x(self):
        self.position.x += self.velocity.x * self.frametime
        if self.should_wrap_screen.x:
            self._wrap_around_screen_x()
        self.rect.centerx = self.position.centerx

    def _set_new_physics_state_and_transform_y(self):
        self.position.y += self.velocity.y * self.frametime
        if self.should_wrap_screen.y:
            self._wrap_around_screen_y()
        self.rect.centery = self.position.centery

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

    def _move_x_back_if_collided(self, sprite_collided):
        if sprite_collided is not None:
            if sprite_collided["side"] == "right":
                self.position.right = sprite_collided["sprite"].rect.left
            if sprite_collided["side"] == "left":
                self.position.left = sprite_collided["sprite"].rect.right
            self.rect.centerx = self.position.centerx

    def _move_y_back_if_collided(self, sprite_collided):
        if sprite_collided is not None:
            if sprite_collided["side"] == "bottom":
                self.position.bottom = sprite_collided["sprite"].rect.top
            if sprite_collided["side"] == "top":
                self.position.top = sprite_collided["sprite"].rect.bottom
            self.rect.centery = self.position.centery

    def _apply_bounce_x(self, sprite_collided):
        if sprite_collided["side"] == "right" and self.should_bounce.east:
            self.constant_velocity_delta.x *= -1
        elif sprite_collided["side"] == "left" and self.should_bounce.west:
            self.constant_velocity_delta.x *= -1

    def _apply_bounce_y(self, sprite_collided):
        if sprite_collided["side"] == "top" and self.should_bounce.north:
            self.constant_velocity_delta.y *= -1
        elif sprite_collided["side"] == "bottom" and self.should_bounce.south:
            self.constant_velocity_delta.y *= -1

    def ensure_velocity_does_not_exceed_maximum(self):
        if self.velocity.x != 0 and self.velocity.y != 0:
            self.velocity.x *= math.cos(math.pi / 4)
            self.velocity.y *= math.sin(math.pi / 4)