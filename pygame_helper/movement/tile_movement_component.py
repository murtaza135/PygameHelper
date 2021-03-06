import pygame
from pygame.math import Vector2
from pygame_helper.rotator2 import Rotator2
from pygame_helper.positional_rect import PositionalRect
from pygame_helper.keybinder import Keybinder
from pygame_helper.movement.abstract_movement_component import AbstractMovementComponent
from pygame_helper.utilities import WHTuple, XYTuple, NESWTuple
import math


# TODO possibly convert this to be dependant on the clock
# and to use pygame.time.delay or pygame.time.wait


class TileMovementComponent(AbstractMovementComponent):
    
    def __init__(self, game_mode, parent_sprite, rect, constant_velocity_delta, tile_geometry,
                default_position=(0, 0), default_rotation=0, default_velocity_delta=None,
                window_size=(800, 600), should_wrap_screen=(True, True),
                should_bounce=(False, False, False, False),
                movement_type="eight_way_movement", direction_control="direction_and_magnitude",
                direction_control_y="direction_and_magnitude"):

        super().__init__(game_mode, parent_sprite, rect)
        self.window_size = WHTuple(*window_size)
        self.tile_geometry = WHTuple(*tile_geometry)

        self.position = PositionalRect(self.rect)
        self.tile_position = default_position
        self.velocity = Vector2()
        self.constant_velocity_delta = Vector2()
        self.tile_constant_velocity_delta = constant_velocity_delta
        self._set_default_velocity_delta(constant_velocity_delta, default_velocity_delta)
        self.rotation = Rotator2(default_rotation)

        self.movement_type = movement_type
        self.direction_control = direction_control
        self.direction_control_y = direction_control_y
        self.check_direction_control_y_for_eight_way_movement()

        self.should_bounce = NESWTuple(*should_bounce)
        self.should_wrap_screen = XYTuple(*should_wrap_screen)

        self.keybinder = Keybinder("right", "left", "down", "up")

    def _set_default_velocity_delta(self, constant_velocity_delta, default_velocity_delta):
        self.default_velocity_delta = Vector2()
        if default_velocity_delta is not None:
            self.tile_default_velocity_delta = default_velocity_delta
        else:
            self.tile_default_velocity_delta = constant_velocity_delta

    @property
    def pixel_position(self):
        return Vector2(self.position.x, self.position.y)

    @pixel_position.setter
    def pixel_position(self, position):
        self.position.x = position[0]
        self.position.y = position[1]
        self.rect.x = (position[0] // self.tile_geometry.width) * self.tile_geometry.width
        self.rect.y = (position[1] // self.tile_geometry.height) * self.tile_geometry.height

    @property
    def tile_position(self):
        return Vector2(
            self.position.x // self.tile_geometry.width,
            self.position.y // self.tile_geometry.height
        )

    @tile_position.setter
    def tile_position(self, position):
        self.position.x = position[0] * self.tile_geometry.width
        self.position.y = position[1] * self.tile_geometry.height
        self.rect.x = position[0] * self.tile_geometry.width
        self.rect.y = position[1] * self.tile_geometry.height

    @property
    def tile_velocity(self):
        return Vector2(
            self.velocity.x / self.tile_geometry.width,
            self.velocity.y / self.tile_geometry.height
        )

    @tile_velocity.setter
    def tile_velocity(self, velocity):
        self.velocity.x = velocity[0] * self.tile_geometry.width
        self.velocity.y = velocity[1] * self.tile_geometry.height

    @property
    def tile_constant_velocity_delta(self):
        return Vector2(
            self.constant_velocity_delta.x / self.tile_geometry.width,
            self.constant_velocity_delta.y / self.tile_geometry.height
        )

    @tile_constant_velocity_delta.setter
    def tile_constant_velocity_delta(self, constant_velocity_delta):
        self.constant_velocity_delta.x = constant_velocity_delta[0] * self.tile_geometry.width
        self.constant_velocity_delta.y = constant_velocity_delta[1] * self.tile_geometry.height

    @property
    def tile_default_velocity_delta(self):
        return Vector2(
            self.default_velocity_delta.x / self.tile_geometry.width,
            self.default_velocity_delta.y / self.tile_geometry.height
        )

    @tile_default_velocity_delta.setter
    def tile_default_velocity_delta(self, default_velocity_delta):
        self.default_velocity_delta.x = default_velocity_delta[0] * self.tile_geometry.width
        self.default_velocity_delta.y = default_velocity_delta[1] * self.tile_geometry.height


    ### Movement Section: Sets physics states & transforms depending upon input and collisions ###
    def move(self):
        self._reset_velocity()
        self._process_movement_input()
        self._set_new_physics_state_and_transform_x()
        self._set_new_physics_state_and_transform_y()

    def move_with_collision(self, collide_fn_x, collide_fn_y, group, dokill=None, collide_callback=None):
        self._reset_velocity()
        self._process_movement_input()
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

    def _reset_velocity(self):
        self.velocity.x = self.constant_velocity_delta.x
        self.velocity.y = self.constant_velocity_delta.y

    def _set_new_physics_state_and_transform_x(self):
        self.position.x += self.velocity.x * self.frametime
        if self.should_wrap_screen.x:
            self.wrap_around_screen_x()
        self.rect.x = self.tile_position.x * self.tile_geometry.width

    def _set_new_physics_state_and_transform_y(self):
        self.position.y += self.velocity.y * self.frametime
        if self.should_wrap_screen.y:
            self.wrap_around_screen_y()
        self.rect.y = self.tile_position.y * self.tile_geometry.height

    def set_pixel_position_to_beginning_of_tile(self):
        self.pixel_position = Vector2(
            self.tile_position.x * self.tile_geometry.width,
            self.tile_position.y * self.tile_geometry.height,
        )

    def wrap_around_screen_x(self):
        if self.position.x >= self.window_size.width:
            self.position.x -= self.window_size.width
        elif self.position.x < 0:
            self.position.x += self.window_size.width

    def wrap_around_screen_y(self):
        if self.position.y >= self.window_size.height:
            self.position.y -= self.window_size.height
        elif self.position.y < 0:
            self.position.y += self.window_size.height

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
    
    def _ensure_velocity_does_not_exceed_maximum(self):
        if self.velocity.x != 0 and self.velocity.y != 0:
            if abs(self.velocity.x) > abs(self.velocity.y):
                bigger_velocity = abs(self.velocity.x)
            else:
                bigger_velocity = abs(self.velocity.y)

            constant_which_x_and_y_are_multiplied_by = bigger_velocity / (math.sqrt(self.velocity.x**2 + self.velocity.y**2))
            self.velocity.x *= constant_which_x_and_y_are_multiplied_by
            self.velocity.y *= constant_which_x_and_y_are_multiplied_by


    ### Input Section: change acceleration, velocity and/or rotation DIRECTLY from input ###
    def _process_movement_input(self):
        if self.movement_type == AbstractMovementComponent.FOUR_WAY_MOVEMENT:
            if self.direction_control == AbstractMovementComponent.DIRECTION_AND_MAGNITUDE:
                self._apply_velocity_in_one_direction_only()
            elif self.direction_control == AbstractMovementComponent.DIRECTION_ONLY:
                self._change_absolute_direction()

        elif self.movement_type == AbstractMovementComponent.EIGHT_WAY_MOVEMENT:
            if self.direction_control == AbstractMovementComponent.DIRECTION_AND_MAGNITUDE:
                self._apply_velocity_x()
            elif self.direction_control == AbstractMovementComponent.DIRECTION_ONLY:
                self._change_direction_x()

            if self.direction_control_y == AbstractMovementComponent.DIRECTION_AND_MAGNITUDE:
                self._apply_velocity_y()
            elif self.direction_control_y == AbstractMovementComponent.DIRECTION_ONLY:
                self._change_direction_y()

            self._ensure_velocity_does_not_exceed_maximum()

    def _apply_velocity_in_one_direction_only(self):
        self.keybinder.track_keys_for_multiple_options("right", "left", "up", "down")
        self.keybinder.update_pressed_keys_order()

        if self.keybinder.is_key_most_recently_pressed_for_option("left"):
            self.velocity.x -= self.keybinder.get_value_for_option("left") * self.tile_geometry.width
            self.velocity.y = 0
        if self.keybinder.is_key_most_recently_pressed_for_option("right"):
            self.velocity.x += self.keybinder.get_value_for_option("right") * self.tile_geometry.width
            self.velocity.y = 0
        if self.keybinder.is_key_most_recently_pressed_for_option("up"):
            self.velocity.y -= self.keybinder.get_value_for_option("up") * self.tile_geometry.height
            self.velocity.x = 0
        if self.keybinder.is_key_most_recently_pressed_for_option("down"):
            self.velocity.y += self.keybinder.get_value_for_option("down") * self.tile_geometry.height
            self.velocity.x = 0

    def _change_absolute_direction(self):
        if self.keybinder.is_key_pressed_for_option("left"):
            self.constant_velocity_delta.x = -abs(self.default_velocity_delta.x)
            self.constant_velocity_delta.y = 0
            self.velocity.y = 0
        elif self.keybinder.is_key_pressed_for_option("right"):
            self.constant_velocity_delta.x = abs(self.default_velocity_delta.x)
            self.constant_velocity_delta.y = 0
            self.velocity.y = 0
        elif self.keybinder.is_key_pressed_for_option("up"):
            self.constant_velocity_delta.x = 0
            self.constant_velocity_delta.y = -abs(self.default_velocity_delta.y)
            self.velocity.x = 0
        elif self.keybinder.is_key_pressed_for_option("down"):
            self.constant_velocity_delta.x = 0
            self.constant_velocity_delta.y = abs(self.default_velocity_delta.y)
            self.velocity.x = 0

    def _apply_velocity_x(self):
        if self.keybinder.is_key_pressed_for_option("left"):
            self.velocity.x -= self.keybinder.get_value_for_option("left") * self.tile_geometry.width
        if self.keybinder.is_key_pressed_for_option("right"):
            self.velocity.x += self.keybinder.get_value_for_option("right") * self.tile_geometry.width

    def _change_direction_x(self):
        if self.keybinder.is_key_pressed_for_option("left"):
            self.constant_velocity_delta.x = -abs(self.constant_velocity_delta.x)
        elif self.keybinder.is_key_pressed_for_option("right"):
            self.constant_velocity_delta.x = abs(self.constant_velocity_delta.x)
        self.velocity.x = self.constant_velocity_delta.x

    def _apply_velocity_y(self):
        if self.keybinder.is_key_pressed_for_option("up"):
            self.velocity.y -= self.keybinder.get_value_for_option("up") * self.tile_geometry.height
        if self.keybinder.is_key_pressed_for_option("down"):
            self.velocity.y += self.keybinder.get_value_for_option("down") * self.tile_geometry.height

    def _change_direction_y(self):
        if self.keybinder.is_key_pressed_for_option("up"):
            self.constant_velocity_delta.y = -abs(self.constant_velocity_delta.y)
        elif self.keybinder.is_key_pressed_for_option("down"):
            self.constant_velocity_delta.y = abs(self.constant_velocity_delta.y)
        self.velocity.y = self.constant_velocity_delta.y


    ### Collision Section: Only DETECTS collision, no movement occurs ###
    def get_x_collision(self, group, dokill=False, collide_callback=None):
        sprite_collided = self.get_collision_right(group, dokill, collide_callback)
        if sprite_collided is not None:
            return sprite_collided
        else:
            return self.get_collision_left(group, dokill, collide_callback)

    def get_collision_right(self, group, dokill=False, collide_callback=None):
        if self.velocity.x > 0:
            self.rect.x += self.tile_geometry.width
            sprites_collided = pygame.sprite.spritecollide(self.parent_sprite, group, dokill, collide_callback)
            self.rect.x -= self.tile_geometry.width
            if sprites_collided:
                return {"sprite": sprites_collided[0], "side": "right"}
        return None

    def get_collision_left(self, group, dokill=False, collide_callback=None):
        if self.velocity.x < 0:
            self.rect.x -= self.tile_geometry.width
            sprites_collided = pygame.sprite.spritecollide(self.parent_sprite, group, dokill, collide_callback)
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
            sprites_collided = pygame.sprite.spritecollide(self.parent_sprite, group, dokill, collide_callback)
            self.rect.y -= self.tile_geometry.height
            if sprites_collided:
                return {"sprite": sprites_collided[0], "side": "bottom"}
        return None

    def get_collision_top(self, group, dokill=False, collide_callback=None):
        if self.velocity.y < 0:
            self.rect.y -= self.tile_geometry.height
            sprites_collided = pygame.sprite.spritecollide(self.parent_sprite, group, dokill, collide_callback)
            self.rect.y += self.tile_geometry.height
            if sprites_collided:
                return {"sprite": sprites_collided[0], "side": "top"}
        return None