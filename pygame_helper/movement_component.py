import pygame
from pygame.math import Vector2
from rotator2 import Rotator2
from keybinder import Keybinder
from utilities import WHTuple, XYTuple, NESWTuple
from positional_rect import PositionalRect


# TODO add rotational movement
# TODO clean up code and separate into classes
# TODO add ability to jump from all 4 sides
# TODO make attributes private, and set saved_acceleration_delta when constant_acceleration_delta is set
# TODO stop movement going faster than what it should be when both x and y movement is occuring


class MovementComponent(object):

    ACCELERATION = "acceleration"
    DIRECTION = "direction"

    FOUR_WAY_MOVEMENT = "four_way_movement"
    EIGHT_WAY_MOVEMENT = "eight_way_movement"
    ROTATIONAL_MOVEMENT = "rotational_movement"

    DIRECTION_ONLY = "direction_only"
    DIRECTION_AND_MAGNITUDE = "direction_and_magnitude"
    
    def __init__(self, parent, rect, constant_acceleration_delta, friction, default_position=(0, 0), 
                default_velocity=(0, 0), default_rotation=Rotator2.RIGHT,
                window_size=(800, 600), bounce_velocity_ratios=(0, 0, 0, 0), should_wrap_screen=(True, True),
                movement_type="eight_way_movement", direction_control=("direction_and_magnitude", "direction_and_magnitude")):
        self.parent = parent
        self.rect = rect
        self.rect.centerx, self.rect.centery = default_position[0], default_position[1]
        self.window_size = WHTuple(*window_size)

        self.position = PositionalRect(self.rect)
        self.velocity = Vector2(default_velocity)
        self.acceleration = Vector2()
        self.friction = Vector2(friction)
        self.constant_acceleration_delta = Vector2(constant_acceleration_delta)
        self.saved_acceleration_delta = Vector2(constant_acceleration_delta)
        self.rotation = Rotator2(default_rotation)

        self._keybinds = Keybinder("right", "left", "down", "up", "jump")

        ratios_made_negative_or_zero = [-abs(ratio) for ratio in bounce_velocity_ratios]
        self.bounce_velocity_ratios = NESWTuple(*ratios_made_negative_or_zero)
        self.should_wrap_screen = XYTuple(*should_wrap_screen)

        self.movement_type = movement_type
        self.direction_control = XYTuple(*direction_control)

    @property
    def keybinds(self):
        return self._keybinds

    @property
    def tick(self):
        tick_ms = self.parent.game_mode.game.clock.get_time()
        tick_seconds = tick_ms / 1000
        return tick_seconds


    def move(self):
        self.acceleration.x = self.constant_acceleration_delta.x
        self.acceleration.y = self.constant_acceleration_delta.y
        self._process_input()

        self._set_new_physics_state_and_transform_x()
        self._set_new_physics_state_and_transform_y()

    def move_with_collision(self, collide_fn_x, collide_fn_y, group, dokill=None, collide_callback=None):
        self.acceleration.x = self.constant_acceleration_delta.x
        self.acceleration.y = self.constant_acceleration_delta.y
        self._process_input()

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


    def _process_input(self):
        if self.movement_type == MovementComponent.ROTATIONAL_MOVEMENT:
            self._apply_rotation()
        elif self.movement_type == MovementComponent.FOUR_WAY_MOVEMENT:
            if self.direction_control.x == MovementComponent.DIRECTION_AND_MAGNITUDE:
                self._apply_acceleration_in_one_direction_only()
            elif self.direction_control.x == MovementComponent.DIRECTION_ONLY:
                self._change_absolute_direction()
        elif self.movement_type == MovementComponent.EIGHT_WAY_MOVEMENT:
            if self.direction_control.x == MovementComponent.DIRECTION_AND_MAGNITUDE:
                self._apply_acceleration_x()
            elif self.direction_control.x == MovementComponent.DIRECTION_ONLY:
                self._change_direction_x()

            if self.direction_control.y == MovementComponent.DIRECTION_AND_MAGNITUDE:
                self._apply_acceleration_y()
            elif self.direction_control.y == MovementComponent.DIRECTION_ONLY:
                self._change_direction_y()

    def _apply_rotation(self):
        # pressed_keys = pygame.key.get_pressed()

        if self.keybinds.is_key_pressed_for_option("left"):
            self.rotation.rotator -= self.keybinds.get_value_for_option("left") * self.tick
        if self.keybinds.is_key_pressed_for_option("right"):
            self.rotation.rotator += self.keybinds.get_value_for_option("right") * self.tick
        if self.keybinds.is_key_pressed_for_option("up"):
            self.acceleration.x += self.keybinds.get_value_for_option("up")
            self.acceleration = self.acceleration.rotate(self.rotation.rotator)
        if self.keybinds.is_key_pressed_for_option("down"):
            self.acceleration.x -= self.keybinds.get_value_for_option("down")
            self.acceleration = self.acceleration.rotate(self.rotation.rotator)

        self.parent.image = pygame.transform.rotate(self.parent.original_image, -self.rotation.rotator)
        self.parent.rect = self.parent.image.get_rect()
        self.rect = self.parent.rect
        self.rect.centerx, self.rect.centery = self.position.centerx, self.position.centery


        # print(self.acceleration)
        # print(self.rotation)
            

    def _apply_acceleration_in_one_direction_only(self):
        self.keybinds.update_pressed_keys_order()

        if self.keybinds.is_key_most_recently_pressed_for_option("left"):
            self.acceleration.x -= self.keybinds.get_value_for_option("left")
            self.velocity.y = 0
        if self.keybinds.is_key_most_recently_pressed_for_option("right"):
            self.acceleration.x += self.keybinds.get_value_for_option("right")
            self.velocity.y = 0
        if self.keybinds.is_key_most_recently_pressed_for_option("up"):
            self.acceleration.y -= self.keybinds.get_value_for_option("up")
            self.velocity.x = 0
        if self.keybinds.is_key_most_recently_pressed_for_option("down"):
            self.acceleration.y += self.keybinds.get_value_for_option("down")
            self.velocity.x = 0

    def _change_absolute_direction(self):
        pressed_keys = pygame.key.get_pressed()

        if self.keybinds.is_key_pressed_for_option("left", pressed_keys):
            self.constant_acceleration_delta.x = -abs(self.saved_acceleration_delta.x)
            self.constant_acceleration_delta.y = 0
            self.velocity.y = 0
        elif self.keybinds.is_key_pressed_for_option("right", pressed_keys):
            self.constant_acceleration_delta.x = abs(self.saved_acceleration_delta.x)
            self.constant_acceleration_delta.y = 0
            self.velocity.y = 0
        elif self.keybinds.is_key_pressed_for_option("up", pressed_keys):
            self.constant_acceleration_delta.y = -abs(self.saved_acceleration_delta.y)
            self.constant_acceleration_delta.x = 0
            self.velocity.x = 0
        elif self.keybinds.is_key_pressed_for_option("down", pressed_keys):
            self.constant_acceleration_delta.y = abs(self.saved_acceleration_delta.y)
            self.constant_acceleration_delta.x = 0
            self.velocity.x = 0

    def _apply_acceleration_x(self):
        pressed_keys = pygame.key.get_pressed()

        if self.keybinds.is_key_pressed_for_option("left", pressed_keys):
            self.acceleration.x -= self.keybinds.get_value_for_option("left")
        if self.keybinds.is_key_pressed_for_option("right", pressed_keys):
            self.acceleration.x += self.keybinds.get_value_for_option("right")

    def _change_direction_x(self):
        pressed_keys = pygame.key.get_pressed()

        if self.keybinds.is_key_pressed_for_option("left", pressed_keys):
            self.constant_acceleration_delta.x = -abs(self.constant_acceleration_delta.x)
        elif self.keybinds.is_key_pressed_for_option("right", pressed_keys):
            self.constant_acceleration_delta.x = abs(self.constant_acceleration_delta.x)
        self.acceleration.x = self.constant_acceleration_delta.x

    def _apply_acceleration_y(self):
        pressed_keys = pygame.key.get_pressed()

        if self.keybinds.is_key_pressed_for_option("up", pressed_keys):
            self.acceleration.y -= self.keybinds.get_value_for_option("up")
        if self.keybinds.is_key_pressed_for_option("down", pressed_keys):
            self.acceleration.y += self.keybinds.get_value_for_option("down")

    def _change_direction_y(self):
        pressed_keys = pygame.key.get_pressed()

        if self.keybinds.is_key_pressed_for_option("up", pressed_keys):
            self.constant_acceleration_delta.y = -abs(self.constant_acceleration_delta.y)
        elif self.keybinds.is_key_pressed_for_option("down", pressed_keys):
            self.constant_acceleration_delta.y = abs(self.constant_acceleration_delta.y)
        self.acceleration.y = self.constant_acceleration_delta.y

    def _jump_if_key_pressed(self):
        if self.keybinds.is_key_pressed_for_option("jump"):
            self.velocity.y = -abs(self.keybinds.get_value_for_option("jump"))

    
    def _set_new_physics_state_and_transform_x(self):
        self.acceleration.x += self.velocity.x * self.friction.x
        self.velocity.x += self.acceleration.x * self.tick
        self.position.x += (self.velocity.x * self.tick) + (0.5 * self.acceleration.x * self.tick**2)
        if self.should_wrap_screen.x:
            self._wrap_around_screen_x()
        self.rect.centerx = self.position.centerx

    def _set_new_physics_state_and_transform_y(self):
        self.acceleration.y += self.velocity.y * self.friction.y
        self.velocity.y += self.acceleration.y * self.tick
        self.position.y += (self.velocity.y * self.tick) + (0.5 * self.acceleration.y * self.tick**2)
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
            self._jump_if_key_pressed()


    def get_x_collision(self, group, dokill=False, collide_callback=None):
        sprite_collided = self.get_collision_right(group, dokill, collide_callback)
        if sprite_collided is not None:
            return sprite_collided
        else:
            return self.get_collision_left(group, dokill, collide_callback)

    def get_collision_right(self, group, dokill=False, collide_callback=None):
        if collide_callback == None:
            collide_callback = MovementComponent.collide_positionalrect

        if self.velocity.x > 0 or (self.velocity.x == 0 and self.acceleration.x > 0):
            sprites_collided = pygame.sprite.spritecollide(self.parent, group, dokill, collide_callback)
            if sprites_collided:
                return {"sprite": sprites_collided[0], "side": "right"}
        return None

    def get_collision_left(self, group, dokill=False, collide_callback=None):
        if collide_callback == None:
            collide_callback = MovementComponent.collide_positionalrect

        if self.velocity.x < 0 or (self.velocity.x == 0 and self.acceleration.x < 0):
            sprites_collided = pygame.sprite.spritecollide(self.parent, group, dokill, collide_callback)
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
            collide_callback = MovementComponent.collide_positionalrect

        if self.velocity.y > 0 or (self.velocity.y == 0 and self.acceleration.y > 0):
            sprites_collided = pygame.sprite.spritecollide(self.parent, group, dokill, collide_callback)
            if sprites_collided:
                return {"sprite": sprites_collided[0], "side": "bottom"}
        return None

    def get_collision_top(self, group, dokill=False, collide_callback=None):
        if collide_callback == None:
            collide_callback = MovementComponent.collide_positionalrect

        if self.velocity.y < 0 or (self.velocity.y == 0 and self.acceleration.y < 0):
            sprites_collided = pygame.sprite.spritecollide(self.parent, group, dokill, collide_callback)
            if sprites_collided:
                return {"sprite": sprites_collided[0], "side": "top"}
        return None

    def spritecollide(self, group):
        return [sprite for sprite in group if self.position.colliderect(sprite.rect)]

    @staticmethod
    def collide_positionalrect(sprite_one, sprite_two):
        return sprite_one.movement.position.rect.colliderect(sprite_two.rect)