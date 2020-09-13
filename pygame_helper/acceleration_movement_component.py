import pygame
from pygame.math import Vector2
from rotator2 import Rotator2
from positional_rect import PositionalRect
from keybinder import Keybinder
from movement_component import MovementComponent
from acceleration_input_component import AccelerationInputComponent
from acceleration_collision_component import AccelerationCollisionComponent
from utilities import WHTuple, XYTuple, NESWTuple


# TODO clean up code and separate into classes, make better names
# TODO make attributes private, and ability to change certain attributes only
# TODO stop movement going faster than what it should be when both x and y movement is occuring
# TODO add ability to jump from all 4 sides


class AccelerationMovementComponent(MovementComponent):

    def __init__(self, parent, rect, constant_acceleration_delta, friction, default_position=(0, 0),
                default_acceleration_delta=(0, 0), default_rotation=0, window_size=(800, 600),
                should_wrap_screen=(True, True), bounce_velocity_ratios=(0, 0, 0, 0),
                movement_type="eight_way_movement", direction_control="direction_and_magnitude", direction_control_y=None):
        self.parent = parent
        self.rect = rect
        self.rect.center = (default_position[0], default_position[1])
        self.window_size = WHTuple(*window_size)

        self.position = PositionalRect(self.rect)
        self.velocity = Vector2()
        self.acceleration = Vector2()
        self.friction = Vector2(-abs(friction[0]), -abs(friction[1]))
        self.constant_acceleration_delta = Vector2(constant_acceleration_delta)
        self.default_acceleration_delta = Vector2(default_acceleration_delta)
        self.rotation = Rotator2(default_rotation)

        ratios_made_negative_or_zero = [-abs(ratio) for ratio in bounce_velocity_ratios]
        self.bounce_velocity_ratios = NESWTuple(*ratios_made_negative_or_zero)
        self.should_wrap_screen = XYTuple(*should_wrap_screen)

        self._keybinder = Keybinder("right", "left", "down", "up", "jump")
        self._movement_input = AccelerationInputComponent(self, self._keybinder, movement_type, direction_control, direction_control_y)
        self._collision = AccelerationCollisionComponent(self)

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
        self._reset_acceleration()
        self._movement_input.process_movement_input()
        self._set_new_physics_state_and_transform_x()
        self._set_new_physics_state_and_transform_y()

    def move_with_collision(self, collide_fn_x, collide_fn_y, group, dokill=None, collide_callback=None):
        self._reset_acceleration()
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
            self._apply_bounce_or_jump_x(sprite_collided)

    def _move_y_with_collision(self, collide_fn, group, dokill=None, collide_callback=None):
        self._set_new_physics_state_and_transform_y()

        sprite_collided = None
        if collide_fn is not None:
            sprite_collided = collide_fn(group, dokill, collide_callback)

        if sprite_collided is not None:
            self._move_y_back_if_collided(sprite_collided)
            self._apply_bounce_or_jump_y(sprite_collided)


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

    def _apply_bounce_or_jump_x(self, sprite_collided):
        if sprite_collided["side"] == "right":
            self.velocity.x *= self.bounce_velocity_ratios.east
        elif sprite_collided["side"] == "left":
            self.velocity.x *= self.bounce_velocity_ratios.west

    def _apply_bounce_or_jump_y(self, sprite_collided):
        if sprite_collided["side"] == "top":
            self.velocity.y *= self.bounce_velocity_ratios.north
        elif sprite_collided["side"] == "bottom":
            self.velocity.y *= self.bounce_velocity_ratios.south
            self._movement_input.set_jump_velocity_if_key_pressed()