import pygame
from pygame.math import Vector2
from pygame_helper import Rotator2
from positional_rect import PositionalRect
from keybinder import Keybinder
from movement_component import MovementComponent
from utilities import WHTuple, XYTuple, NESWTuple
import math


class TileMovementComponent(MovementComponent):
    
    def __init__(self, parent, rect, tile_geometry, constant_velocity_delta, default_position=(0, 0), 
                default_velocity_delta=(0, 0), default_rotation=0, window_size=(800, 600), should_bounce=(False, False, False, False),
                should_wrap_screen=(True, True), movement_type="eight_way_movement",
                direction_control=("direction_and_magnitude", "direction_and_magnitude")):
        self.parent = parent
        self.tile_geometry = WHTuple(*tile_geometry)
        self.window_size = WHTuple(*window_size)
        self.rect = rect
        self.rect.x = default_position[0] * self.tile_geometry.width
        self.rect.y = default_position[1] * self.tile_geometry.height

        self.position = PositionalRect(self.rect)
        self.velocity = Vector2()
        self.constant_velocity_delta = Vector2()
        self.set_tile_constant_velocity_delta(constant_velocity_delta)
        self.default_velocity_delta = Vector2()
        self.set_tile_default_velocity_delta(default_velocity_delta)
        self.rotation = Rotator2(default_rotation)

        self._keybinder = Keybinder("right", "left", "down", "up")

        self.should_bounce = NESWTuple(*should_bounce)
        self.should_wrap_screen = XYTuple(*should_wrap_screen)

        self.movement_type = movement_type
        self.direction_control = XYTuple(*direction_control)

    @property
    def keybinds(self):
        return self._keybinder

    @property
    def frametime(self):
        frametime_ms = self.parent.game_mode.game.clock.get_time()
        frametime_seconds = frametime_ms / 1000
        return frametime_seconds

    def get_tile_position(self):
        return Vector2(
            math.floor(self.position.x / self.tile_geometry.width),
            math.floor(self.position.y / self.tile_geometry.height)
        )

    def set_tile_position(self, position):
        self.position.x = position[0] * self.tile_geometry.width
        self.position.y = position[1] * self.tile_geometry.height
        self.rect.x = position[0] * self.tile_geometry.width
        self.rect.y = position[1] * self.tile_geometry.height

    def get_tile_velocity(self):
        return Vector2(
            self.velocity.x / self.tile_geometry.width,
            self.velocity.y / self.tile_geometry.height
        )

    def set_tile_velocity(self, velocity):
        self.velocity.x = velocity[0] * self.tile_geometry.width
        self.velocity.y = velocity[1] * self.tile_geometry.height

    def get_tile_constant_velocity_delta(self):
        return Vector2(
            self.constant_velocity_delta.x / self.tile_geometry.width,
            self.constant_velocity_delta.y / self.tile_geometry.height
        )

    def set_tile_constant_velocity_delta(self, constant_velocity_delta):
        self.constant_velocity_delta.x = constant_velocity_delta[0] * self.tile_geometry.width
        self.constant_velocity_delta.y = constant_velocity_delta[1] * self.tile_geometry.height

    def get_tile_default_velocity_delta(self):
        return Vector2(
            self.default_velocity_delta.x / self.tile_geometry.width,
            self.default_velocity_delta.y / self.tile_geometry.height
        )

    def set_tile_default_velocity_delta(self, default_velocity_delta):
        self.default_velocity_delta.x = default_velocity_delta[0] * self.tile_geometry.width
        self.default_velocity_delta.y = default_velocity_delta[1] * self.tile_geometry.height


    def move(self):
        self._reset_velocity()
        self._process_input_into_velocity_changes()
        self._set_new_physics_state_and_transform_x()
        self._set_new_physics_state_and_transform_y()

    def move_with_collision(self, collide_fn_x, collide_fn_y, group, dokill=None, collide_callback=None):
        self._reset_velocity()
        self._process_input_into_velocity_changes()
        self._move_x_with_collision(collide_fn_x, group, dokill, collide_callback)
        self._move_y_with_collision(collide_fn_y, group, dokill, collide_callback)

    def _move_x_with_collision(self, collide_fn, group, dokill=None, collide_callback=None):
        sprite_collided = None
        if collide_fn is not None:
            sprite_collided = collide_fn(group, dokill, collide_callback)

        if sprite_collided is None:
            self._set_new_physics_state_and_transform_x()
        else:
            self._apply_bounce_x(sprite_collided)

    def _move_y_with_collision(self, collide_fn, group, dokill=None, collide_callback=None):
        sprite_collided = None
        if collide_fn is not None:
            sprite_collided = collide_fn(group, dokill, collide_callback)

        if sprite_collided is None:
            self._set_new_physics_state_and_transform_y()
        else:
            self._apply_bounce_y(sprite_collided)


    def _process_input_into_velocity_changes(self):
        if self.movement_type == TileMovementComponent.FOUR_WAY_MOVEMENT:
            if self.direction_control.x == TileMovementComponent.DIRECTION_AND_MAGNITUDE:
                self._apply_velocity_in_one_direction_only()
            elif self.direction_control.x == TileMovementComponent.DIRECTION_ONLY:
                self._change_absolute_direction()

        elif self.movement_type == TileMovementComponent.EIGHT_WAY_MOVEMENT:
            if self.direction_control.x == TileMovementComponent.DIRECTION_AND_MAGNITUDE:
                self._apply_velocity_x()
            elif self.direction_control.x == TileMovementComponent.DIRECTION_ONLY:
                self._change_direction_x()

            if self.direction_control.y == TileMovementComponent.DIRECTION_AND_MAGNITUDE:
                self._apply_velocity_y()
            elif self.direction_control.y == TileMovementComponent.DIRECTION_ONLY:
                self._change_direction_y()

            self._set_velocity_to_maximum_in_eight_way_movement()

    def _set_velocity_to_maximum_in_eight_way_movement(self):
        if self.velocity.x != 0 and self.velocity.y != 0:
            self.velocity.x *= math.cos(math.pi / 4)
            self.velocity.y *= math.sin(math.pi / 4)

    def _apply_velocity_in_one_direction_only(self):
        self.keybinds.track_keys_for_multiple_options("right", "left", "up", "down")
        self.keybinds.update_pressed_keys_order()

        if self.keybinds.is_key_most_recently_pressed_for_option("left"):
            self.velocity.x -= self.keybinds.get_value_for_option("left") * self.tile_geometry.width
            self.velocity.y = 0
        if self.keybinds.is_key_most_recently_pressed_for_option("right"):
            self.velocity.x += self.keybinds.get_value_for_option("right") * self.tile_geometry.width
            self.velocity.y = 0
        if self.keybinds.is_key_most_recently_pressed_for_option("up"):
            self.velocity.y -= self.keybinds.get_value_for_option("up") * self.tile_geometry.height
            self.velocity.x = 0
        if self.keybinds.is_key_most_recently_pressed_for_option("down"):
            self.velocity.y += self.keybinds.get_value_for_option("down") * self.tile_geometry.height
            self.velocity.x = 0

    def _change_absolute_direction(self):
        if self.keybinds.is_key_pressed_for_option("left"):
            self.constant_velocity_delta.x = -abs(self.default_velocity_delta.x)
            self.constant_velocity_delta.y = 0
            self.velocity.y = 0
        elif self.keybinds.is_key_pressed_for_option("right"):
            self.constant_velocity_delta.x = abs(self.default_velocity_delta.x)
            self.constant_velocity_delta.y = 0
            self.velocity.y = 0
        elif self.keybinds.is_key_pressed_for_option("up"):
            self.constant_velocity_delta.x = 0
            self.constant_velocity_delta.y = -abs(self.default_velocity_delta.y)
            self.velocity.x = 0
        elif self.keybinds.is_key_pressed_for_option("down"):
            self.constant_velocity_delta.x = 0
            self.constant_velocity_delta.y = abs(self.default_velocity_delta.y)
            self.velocity.x = 0

    def _apply_velocity_x(self):
        if self.keybinds.is_key_pressed_for_option("left"):
            self.velocity.x -= self.keybinds.get_value_for_option("left") * self.tile_geometry.width
        if self.keybinds.is_key_pressed_for_option("right"):
            self.velocity.x += self.keybinds.get_value_for_option("right") * self.tile_geometry.width

    def _change_direction_x(self):
        if self.keybinds.is_key_pressed_for_option("left"):
            self.constant_velocity_delta.x = -abs(self.constant_velocity_delta.x)
        elif self.keybinds.is_key_pressed_for_option("right"):
            self.constant_velocity_delta.x = abs(self.constant_velocity_delta.x)
        self.velocity.x = self.constant_velocity_delta.x

    def _apply_velocity_y(self):
        if self.keybinds.is_key_pressed_for_option("up"):
            self.velocity.y -= self.keybinds.get_value_for_option("up") * self.tile_geometry.height
        if self.keybinds.is_key_pressed_for_option("down"):
            self.velocity.y += self.keybinds.get_value_for_option("down") * self.tile_geometry.height

    def _change_direction_y(self):
        if self.keybinds.is_key_pressed_for_option("up"):
            self.constant_velocity_delta.y = -abs(self.constant_velocity_delta.y)
        elif self.keybinds.is_key_pressed_for_option("down"):
            self.constant_velocity_delta.y = abs(self.constant_velocity_delta.y)
        self.velocity.y = self.constant_velocity_delta.y

    
    def _reset_velocity(self):
        self.velocity.x = self.constant_velocity_delta.x
        self.velocity.y = self.constant_velocity_delta.y

    def _set_new_physics_state_and_transform_x(self):
        self.position.x += self.velocity.x * self.frametime
        if self.should_wrap_screen.x:
            self._wrap_around_screen_x()
        self.rect.x = math.floor(self.position.x / self.tile_geometry.width) * self.tile_geometry.width

    def _set_new_physics_state_and_transform_y(self):
        self.position.y += self.velocity.y * self.frametime
        if self.should_wrap_screen.y:
            self._wrap_around_screen_y()
        self.rect.y = math.floor(self.position.y / self.tile_geometry.height) * self.tile_geometry.height

    def _wrap_around_screen_x(self):
        if self.position.x >= self.window_size.width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = self.window_size.width

    def _wrap_around_screen_y(self):
        if self.position.y >= self.window_size.height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = self.window_size.height

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


    def get_x_collision(self, group, dokill=False, collide_callback=None):
        sprite_collided = self.get_collision_right(group, dokill, collide_callback)
        if sprite_collided is not None:
            return sprite_collided
        else:
            return self.get_collision_left(group, dokill, collide_callback)

    def get_collision_right(self, group, dokill=False, collide_callback=None):
        if self.velocity.x > 0:
            self.rect.x += self.tile_geometry.width
            sprites_collided = pygame.sprite.spritecollide(self.parent, group, dokill, collide_callback)
            self.rect.x -= self.tile_geometry.width
            if sprites_collided:
                return {"sprite": sprites_collided[0], "side": "right"}
        return None

    def get_collision_left(self, group, dokill=False, collide_callback=None):
        if self.velocity.x < 0:
            self.rect.x -= self.tile_geometry.width
            sprites_collided = pygame.sprite.spritecollide(self.parent, group, dokill, collide_callback)
            self.rect.x += self.tile_geometry.width
            if sprites_collided:
                return {"sprite": sprites_collided[0], "side": "left"}
        return None
        
    def get_y_collision(self, group, dokill=False, collide_callback=None):
        sprite_collided = self.get_collision_bottom(group, dokill, collide_callback)
        if sprite_collided is not None:
            return sprite_collided
        else:
            return self.get_collision_top(group, dokill, collide_callback)

    def get_collision_bottom(self, group, dokill=False, collide_callback=None):
        if self.velocity.y > 0:
            self.rect.y += self.tile_geometry.height
            sprites_collided = pygame.sprite.spritecollide(self.parent, group, dokill, collide_callback)
            self.rect.y -= self.tile_geometry.height
            if sprites_collided:
                return {"sprite": sprites_collided[0], "side": "bottom"}
        return None

    def get_collision_top(self, group, dokill=False, collide_callback=None):
        if self.velocity.y < 0:
            self.rect.y -= self.tile_geometry.height
            sprites_collided = pygame.sprite.spritecollide(self.parent, group, dokill, collide_callback)
            self.rect.y += self.tile_geometry.height
            if sprites_collided:
                return {"sprite": sprites_collided[0], "side": "top"}
        return None

    def spritecollide(self, group):
        return [sprite for sprite in group if self.position.colliderect(sprite.rect)]

    @staticmethod
    def collide_positional_rect(sprite_one, sprite_two):
        return sprite_one.movement._position.rect.colliderect(sprite_two.rect)