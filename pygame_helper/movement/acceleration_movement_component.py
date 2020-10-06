import pygame
from pygame.math import Vector2
from pygame_helper.rotator2 import Rotator2
from pygame_helper.positional_rect import PositionalRect
from pygame_helper.input.keybinder import Keybinder
from pygame_helper.movement.abstract_movement_component import AbstractMovementComponent
from pygame_helper.utilities import WHTuple, XYTuple, NESWTuple


class AccelerationMovementComponent(AbstractMovementComponent):

    def __init__(self, game_mode, parent_sprite, rect, constant_acceleration_delta, friction, default_position=(0, 0),
                default_rotation=0, default_acceleration_delta=None, window_size=(800, 600),
                should_wrap_screen=(True, True), bounce_velocity_ratios=(0, 0, 0, 0),
                sides_to_jump=(False, False, True, False), movement_type="eight_way_movement",
                direction_control="direction_and_magnitude", direction_control_y="direction_and_magnitude"):

        super().__init__(game_mode, parent_sprite, rect)
        self.rect.center = (default_position[0], default_position[1])
        self.window_size = WHTuple(*window_size)

        self.position = PositionalRect(self.rect)
        self.velocity = Vector2()
        self.acceleration = Vector2()
        self.friction = Vector2(-abs(friction[0]), -abs(friction[1]))
        self.constant_acceleration_delta = Vector2(constant_acceleration_delta)
        self._set_default_acceleration_delta(constant_acceleration_delta, default_acceleration_delta)
        self.rotation = Rotator2(default_rotation)

        self.movement_type = movement_type
        self.direction_control = direction_control
        self.direction_control_y = direction_control_y
        self.check_direction_control_y_for_eight_way_movement()

        ratios_made_negative_or_zero = [-abs(ratio) for ratio in bounce_velocity_ratios]
        self.bounce_velocity_ratios = NESWTuple(*ratios_made_negative_or_zero)
        self.sides_to_jump = NESWTuple(*sides_to_jump)
        self.should_wrap_screen = XYTuple(*should_wrap_screen)

        self.keybinder = Keybinder("right", "left", "down", "up", "jump")

    def _set_default_acceleration_delta(self, constant_acceleration_delta, default_acceleration_delta):
        if default_acceleration_delta is not None:
            self.default_acceleration_delta = Vector2(default_acceleration_delta)
        else:
            self.default_acceleration_delta = Vector2(constant_acceleration_delta)


    ### Movement Section: Sets physics states & transforms depending upon input and collisions ###
    def move(self):
        self._reset_acceleration()
        self._process_movement_input()
        self._set_new_physics_state_and_transform_x()
        self._set_new_physics_state_and_transform_y()

    def move_with_collision(self, collide_fn_x, collide_fn_y, group, dokill=None, collide_callback=None):
        self._reset_acceleration()
        self._process_movement_input()
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
            self.wrap_around_screen_x()
        self.rect.centerx = self.position.centerx

    def _set_new_physics_state_and_transform_y(self):
        self.acceleration.y += self.velocity.y * self.friction.y
        self.velocity.y += self.acceleration.y * self.frametime
        self.position.y += (self.velocity.y * self.frametime) + (0.5 * self.acceleration.y * self.frametime**2)
        if self.should_wrap_screen.y:
            self.wrap_around_screen_y()
        self.rect.centery = self.position.centery

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
            self._set_jump_velocity_leftwards_if_key_pressed()
        elif sprite_collided["side"] == "left" and self.sides_to_jump.west:
            self._set_jump_velocity_rightwards_if_key_pressed()

    def _apply_jump_y(self, sprite_collided):
        if sprite_collided["side"] == "top" and self.sides_to_jump.north:
            self._set_jump_velocity_downwards_if_key_pressed()
        elif sprite_collided["side"] == "bottom" and self.sides_to_jump.south:
            self._set_jump_velocity_upwards_if_key_pressed()


    ### Input Section: change acceleration, velocity and/or rotation DIRECTLY from input ###
    def _process_movement_input(self):
        if self.movement_type == AbstractMovementComponent.ROTATIONAL_MOVEMENT:
            if self.direction_control == AbstractMovementComponent.DIRECTION_AND_MAGNITUDE:
                self._apply_rotation_and_acceleration()
            elif self.direction_control == AbstractMovementComponent.DIRECTION_ONLY:
                self._apply_rotation_only()
            self._rotate_image_and_rect_at_center()

        elif self.movement_type == AbstractMovementComponent.FOUR_WAY_MOVEMENT:
            if self.direction_control == AbstractMovementComponent.DIRECTION_AND_MAGNITUDE:
                self._apply_acceleration_in_one_direction_only()
            elif self.direction_control == AbstractMovementComponent.DIRECTION_ONLY:
                self._change_absolute_direction()

        elif self.movement_type == AbstractMovementComponent.EIGHT_WAY_MOVEMENT:
            if self.direction_control == AbstractMovementComponent.DIRECTION_AND_MAGNITUDE:
                self._apply_acceleration_x()
            elif self.direction_control == AbstractMovementComponent.DIRECTION_ONLY:
                self._change_direction_x()

            if self.direction_control_y == AbstractMovementComponent.DIRECTION_AND_MAGNITUDE:
                self._apply_acceleration_y()
            elif self.direction_control_y == AbstractMovementComponent.DIRECTION_ONLY:
                self._change_direction_y()

    def _apply_rotation_and_acceleration(self):
        if self.keybinder.is_key_pressed_for_option("left"):
            self.rotation.rotator -= self.keybinder.get_value_for_option("left") * self.frametime
        if self.keybinder.is_key_pressed_for_option("right"):
            self.rotation.rotator += self.keybinder.get_value_for_option("right") * self.frametime
        if self.keybinder.is_key_pressed_for_option("up"):
            self.acceleration.x += self.keybinder.get_value_for_option("up")
            self.acceleration = self.acceleration.rotate(self.rotation.rotator)
        if self.keybinder.is_key_pressed_for_option("down"):
            self.acceleration.x -= self.keybinder.get_value_for_option("down")
            self.acceleration = self.acceleration.rotate(self.rotation.rotator)

    def _apply_rotation_only(self):
        if self.keybinder.is_key_pressed_for_option("left"):
            self.rotation.rotator -= self.keybinder.get_value_for_option("left") * self.frametime
        if self.keybinder.is_key_pressed_for_option("right"):
            self.rotation.rotator += self.keybinder.get_value_for_option("right") * self.frametime
        self.acceleration = self.acceleration.rotate(self.rotation.rotator)

    def _rotate_image_and_rect_at_center(self):
        self.parent_sprite.image = pygame.transform.rotate(
            self.parent_sprite.original_image,
            -self.rotation.rotator
        )
        self.parent_sprite.rect = self.parent_sprite.image.get_rect()
        self.rect = self.parent_sprite.rect
        self.rect.centerx = self.position.centerx
        self.rect.centery = self.position.centery

    def _apply_acceleration_in_one_direction_only(self):
        self.keybinder.track_keys_for_multiple_options("right", "left", "up", "down")
        self.keybinder.update_pressed_keys_order()

        if self.keybinder.is_key_most_recently_pressed_for_option("left"):
            self.acceleration.x -= self.keybinder.get_value_for_option("left")
            self.velocity.y = 0
        if self.keybinder.is_key_most_recently_pressed_for_option("right"):
            self.acceleration.x += self.keybinder.get_value_for_option("right")
            self.velocity.y = 0
        if self.keybinder.is_key_most_recently_pressed_for_option("up"):
            self.acceleration.y -= self.keybinder.get_value_for_option("up")
            self.velocity.x = 0
        if self.keybinder.is_key_most_recently_pressed_for_option("down"):
            self.acceleration.y += self.keybinder.get_value_for_option("down")
            self.velocity.x = 0

    def _change_absolute_direction(self):
        if self.keybinder.is_key_pressed_for_option("left"):
            self.constant_acceleration_delta.x = -abs(self.default_acceleration_delta.x)
            self.constant_acceleration_delta.y = 0
            self.velocity.y = 0
        elif self.keybinder.is_key_pressed_for_option("right"):
            self.constant_acceleration_delta.x = abs(self.default_acceleration_delta.x)
            self.constant_acceleration_delta.y = 0
            self.velocity.y = 0
        elif self.keybinder.is_key_pressed_for_option("up"):
            self.constant_acceleration_delta.x = 0
            self.constant_acceleration_delta.y = -abs(self.default_acceleration_delta.y)
            self.velocity.x = 0
        elif self.keybinder.is_key_pressed_for_option("down"):
            self.constant_acceleration_delta.x = 0
            self.constant_acceleration_delta.y = abs(self.default_acceleration_delta.y)
            self.velocity.x = 0
        
        self.acceleration.x = self.constant_acceleration_delta.x
        self.acceleration.y = self.constant_acceleration_delta.y

    def _apply_acceleration_x(self):
        if self.keybinder.is_key_pressed_for_option("left"):
            self.acceleration.x -= self.keybinder.get_value_for_option("left")
        if self.keybinder.is_key_pressed_for_option("right"):
            self.acceleration.x += self.keybinder.get_value_for_option("right")

    def _change_direction_x(self):
        if self.keybinder.is_key_pressed_for_option("left"):
            self.constant_acceleration_delta.x = -abs(self.constant_acceleration_delta.x)
        elif self.keybinder.is_key_pressed_for_option("right"):
            self.constant_acceleration_delta.x = abs(self.constant_acceleration_delta.x)
        self.acceleration.x = self.constant_acceleration_delta.x

    def _apply_acceleration_y(self):
        if self.keybinder.is_key_pressed_for_option("up"):
            self.acceleration.y -= self.keybinder.get_value_for_option("up")
        if self.keybinder.is_key_pressed_for_option("down"):
            self.acceleration.y += self.keybinder.get_value_for_option("down")

    def _change_direction_y(self):
        if self.keybinder.is_key_pressed_for_option("up"):
            self.constant_acceleration_delta.y = -abs(self.constant_acceleration_delta.y)
        elif self.keybinder.is_key_pressed_for_option("down"):
            self.constant_acceleration_delta.y = abs(self.constant_acceleration_delta.y)
        self.acceleration.y = self.constant_acceleration_delta.y

    def _set_jump_velocity_leftwards_if_key_pressed(self):
        if self.keybinder.is_key_pressed_for_option("jump"):
            self.velocity.x = -abs(self.keybinder.get_value_for_option("jump"))

    def _set_jump_velocity_rightwards_if_key_pressed(self):
        if self.keybinder.is_key_pressed_for_option("jump"):
            self.velocity.x = abs(self.keybinder.get_value_for_option("jump"))

    def _set_jump_velocity_upwards_if_key_pressed(self):
        if self.keybinder.is_key_pressed_for_option("jump"):
            self.velocity.y = -abs(self.keybinder.get_value_for_option("jump"))

    def _set_jump_velocity_downwards_if_key_pressed(self):
        if self.keybinder.is_key_pressed_for_option("jump"):
            self.velocity.y = abs(self.keybinder.get_value_for_option("jump"))


    ### Collision Section: Only DETECTS collision, no movement occurs ###
    def get_x_collision(self, group, dokill=False, collide_callback=None):
        sprite_collided = self.get_collision_right(group, dokill, collide_callback)
        if sprite_collided is not None:
            return sprite_collided
        else:
            return self.get_collision_left(group, dokill, collide_callback)
            
    def get_collision_right(self, group, dokill=False, collide_callback=None):
        if collide_callback == None:
            collide_callback = AbstractMovementComponent.collide_positional_rect

        if self.velocity.x > 0 or (self.velocity.x == 0 and self.acceleration.x > 0):
            sprites_collided = pygame.sprite.spritecollide(self.parent_sprite, group, dokill, collide_callback)
            if sprites_collided:
                return {"sprite": sprites_collided[0], "side": "right"}
        return None

    def get_collision_left(self, group, dokill=False, collide_callback=None):
        if collide_callback == None:
            collide_callback = AbstractMovementComponent.collide_positional_rect

        if self.velocity.x < 0 or (self.velocity.x == 0 and self.acceleration.x < 0):
            sprites_collided = pygame.sprite.spritecollide(self.parent_sprite, group, dokill, collide_callback)
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
        if collide_callback == None:
            collide_callback = AbstractMovementComponent.collide_positional_rect

        if self.velocity.y > 0 or (self.velocity.y == 0 and self.acceleration.y > 0):
            sprites_collided = pygame.sprite.spritecollide(self.parent_sprite, group, dokill, collide_callback)
            if sprites_collided:
                return {"sprite": sprites_collided[0], "side": "bottom"}
        return None

    def get_collision_top(self, group, dokill=False, collide_callback=None):
        if collide_callback == None:
            collide_callback = AbstractMovementComponent.collide_positional_rect

        if self.velocity.y < 0 or (self.velocity.y == 0 and self.acceleration.y < 0):
            sprites_collided = pygame.sprite.spritecollide(self.parent_sprite, group, dokill, collide_callback)
            if sprites_collided:
                return {"sprite": sprites_collided[0], "side": "top"}
        return None