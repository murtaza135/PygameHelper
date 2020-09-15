import pygame
from pygame.math import Vector2
from pygame_helper.input.keybinder import Keybinder
from pygame_helper.movement.abstract_movement_component import AbstractMovementComponent
from pygame_helper.input.velocity_input_component import VelocityInputComponent
from pygame_helper.collision.velocity_collision_component import VelocityCollisionComponent
from pygame_helper.utilities import WHTuple, XYTuple, NESWTuple
import math


class VelocityMovementComponent(AbstractMovementComponent):
    
    def __init__(self, parent, rect, constant_velocity_delta, default_position=(0, 0), 
                default_rotation=0, default_velocity_delta=None, window_size=(800, 600),
                should_wrap_screen=(True, True), should_bounce=(False, False, False, False),
                movement_type="eight_way_movement", direction_control="direction_and_magnitude",
                direction_control_y=None):

        super().__init__(parent, rect, default_position, default_rotation, window_size, should_wrap_screen)
        self.constant_velocity_delta = Vector2(constant_velocity_delta)
        if default_velocity_delta is not None:
            self.default_velocity_delta = Vector2(default_velocity_delta)
        else:
            self.default_velocity_delta = Vector2(constant_velocity_delta)
        self.should_bounce = NESWTuple(*should_bounce)

        self.keybinder = Keybinder("right", "left", "down", "up")
        self.movement_input = VelocityInputComponent(self, self.keybinder, movement_type, direction_control, direction_control_y)
        self.collision = VelocityCollisionComponent(self)

    def move(self):
        self._reset_velocity()
        self.movement_input.process_movement_input()
        self._set_new_physics_state_and_transform_x()
        self._set_new_physics_state_and_transform_y()

    def move_with_collision(self, collide_fn_x, collide_fn_y, group, dokill=None, collide_callback=None):
        self._reset_velocity()
        self.movement_input.process_movement_input()
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
            if abs(self.velocity.x) > abs(self.velocity.y):
                bigger_velocity = abs(self.velocity.x)
            else:
                bigger_velocity = abs(self.velocity.y)

            constant_which_x_and_y_are_multiplied_by = bigger_velocity / (math.sqrt(self.velocity.x**2 + self.velocity.y**2))
            self.velocity.x *= constant_which_x_and_y_are_multiplied_by
            self.velocity.y *= constant_which_x_and_y_are_multiplied_by