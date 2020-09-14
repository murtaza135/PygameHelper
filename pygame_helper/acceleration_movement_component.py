import pygame
from pygame.math import Vector2
from keybinder import Keybinder
from abstract_movement_component import AbstractMovementComponent
from acceleration_input_component import AccelerationInputComponent
from acceleration_collision_component import AccelerationCollisionComponent
from utilities import WHTuple, XYTuple, NESWTuple


class AccelerationMovementComponent(AbstractMovementComponent):

    def __init__(self, parent, rect, constant_acceleration_delta, friction, default_position=(0, 0),
                default_rotation=0, default_acceleration_delta=None, window_size=(800, 600),
                should_wrap_screen=(True, True), bounce_velocity_ratios=(0, 0, 0, 0),
                sides_to_jump=(False, False, True, False), movement_type="eight_way_movement",
                direction_control="direction_and_magnitude", direction_control_y=None):

        super().__init__(parent, rect, default_position, default_rotation, window_size, should_wrap_screen)
        self.acceleration = Vector2()
        self.friction = Vector2(-abs(friction[0]), -abs(friction[1]))
        self.constant_acceleration_delta = Vector2(constant_acceleration_delta)
        if default_acceleration_delta is not None:
            self.default_acceleration_delta = Vector2(default_acceleration_delta)
        else:
            self.default_acceleration_delta = Vector2(constant_acceleration_delta)

        ratios_made_negative_or_zero = [-abs(ratio) for ratio in bounce_velocity_ratios]
        self.bounce_velocity_ratios = NESWTuple(*ratios_made_negative_or_zero)
        self.sides_to_jump = NESWTuple(*sides_to_jump)

        self.keybinder = Keybinder("right", "left", "down", "up", "jump")
        self.movement_input = AccelerationInputComponent(self, self.keybinder, movement_type, direction_control, direction_control_y)
        self.collision = AccelerationCollisionComponent(self)

    def move(self):
        self._reset_acceleration()
        self.movement_input.process_movement_input()
        self._set_new_physics_state_and_transform_x()
        self._set_new_physics_state_and_transform_y()

    def move_with_collision(self, collide_fn_x, collide_fn_y, group, dokill=None, collide_callback=None):
        self._reset_acceleration()
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
            self._apply_jump_x(sprite_collided)

    def _move_y_with_collision(self, collide_fn, group, dokill=None, collide_callback=None):
        self._set_new_physics_state_and_transform_y()

        sprite_collided = None
        if collide_fn is not None:
            sprite_collided = collide_fn(group, dokill, collide_callback)

        if sprite_collided is not None:
            self._move_y_back_if_collided(sprite_collided)
            self._apply_bounce_y(sprite_collided)
            self._apply_jump_y(sprite_collided)

    def _reset_acceleration(self):
        self.acceleration.x = self.constant_acceleration_delta.x
        self.acceleration.y = self.constant_acceleration_delta.y

    def _set_new_physics_state_and_transform_x(self):
        self.acceleration.x += self.velocity.x * self.friction.x
        self.velocity.x += self.acceleration.x * self.frametime
        self.position.x += (self.velocity.x * self.frametime) + (0.5 * self.acceleration.x * self.frametime**2)
        if self.should_wrap_screen.x:
            self._wrap_around_screen_x()
        self.rect.centerx = self.position.centerx

    def _set_new_physics_state_and_transform_y(self):
        self.acceleration.y += self.velocity.y * self.friction.y
        self.velocity.y += self.acceleration.y * self.frametime
        self.position.y += (self.velocity.y * self.frametime) + (0.5 * self.acceleration.y * self.frametime**2)
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
        if sprite_collided["side"] == "right":
            self.velocity.x *= self.bounce_velocity_ratios.east
        elif sprite_collided["side"] == "left":
            self.velocity.x *= self.bounce_velocity_ratios.west

    def _apply_bounce_y(self, sprite_collided):
        if sprite_collided["side"] == "top":
            self.velocity.y *= self.bounce_velocity_ratios.north
        elif sprite_collided["side"] == "bottom":
            self.velocity.y *= self.bounce_velocity_ratios.south

    def _apply_jump_x(self, sprite_collided):
        if sprite_collided["side"] == "right" and self.sides_to_jump.east:
            self.movement_input.set_jump_velocity_leftwards_if_key_pressed()
        elif sprite_collided["side"] == "left" and self.sides_to_jump.west:
            self.movement_input.set_jump_velocity_rightwards_if_key_pressed()

    def _apply_jump_y(self, sprite_collided):
        if sprite_collided["side"] == "top" and self.sides_to_jump.north:
            self.movement_input.set_jump_velocity_downwards_if_key_pressed()
        elif sprite_collided["side"] == "bottom" and self.sides_to_jump.south:
            self.movement_input.set_jump_velocity_upwards_if_key_pressed()