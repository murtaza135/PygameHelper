import pygame
from pygame.math import Vector2
from rotator2 import Rotator2
from keybinder import Keybinder
from utilities import WHGeometry


class TileBasedMovementComponent(object):
    
    def __init__(self, parent, rect, tile_size, friction, default_position=(0, 0), default_rotation=Rotator2.RIGHT,
                default_velocity=(0, 0), default_acceleration=(0, 0), window_size=(800, 600),
                after_bounce_velocity_ratio=0, should_wrap_screen_x=True, should_wrap_screen_y=True):
        self.parent = parent
        self.rect = rect
        self.rect.x, self.rect.y = default_position[0]*tile_size, default_position[1]*tile_size
        self.window_size = WHGeometry(*window_size)

        self.position = self.rect.copy()
        self.rotation = Rotator2(default_rotation)
        self.velocity = Vector2(default_velocity)
        self.acceleration = Vector2(default_acceleration)
        self.friction = Vector2(friction)
        self.start_of_new_frame_acceleration = Vector2(default_acceleration)

        self._keybinds = Keybinder("right", "left", "down", "up", "jump")

        self.after_bounce_velocity_ratio = after_bounce_velocity_ratio
        self.should_wrap_screen_x = should_wrap_screen_x
        self.should_wrap_screen_y = should_wrap_screen_y

    @property
    def keybinds(self):
        return self._keybinds

    @property
    def tick(self):
        tick_ms = self.parent.game_mode.game.clock.get_time()
        tick_seconds = tick_ms / 1000
        return tick_seconds


    def move_without_collision(self):
        self.move_x_without_collision()
        self.move_y_without_collision()

    def move_x_without_collision(self):
        self.acceleration.x = self.start_of_new_frame_acceleration.x
        self.apply_acceleration_x_using_pressed_keys()
        self.acceleration.x += self.velocity.x * self.friction.x
        self.velocity.x += self.acceleration.x
        self.set_new_position_x()

    def move_y_without_collision(self):
        self.acceleration.y = self.start_of_new_frame_acceleration.y
        self.apply_acceleration_y_using_pressed_keys()
        self.acceleration.y += self.velocity.y * self.friction.y
        self.velocity.y += self.acceleration.y
        self.set_new_position_y()

    def move_with_collision(self, collide_fn_x, collide_fn_y, group, dokill=None, collided=None):
        self.move_x_with_collision(collide_fn_x, group, dokill, collided)
        self.move_y_with_collision(collide_fn_y, group, dokill, collided)

    def move_x_with_collision(self, collide_fn, group, dokill=None, collided=None):
        self.acceleration.x = self.start_of_new_frame_acceleration.x
        self.apply_acceleration_x_using_pressed_keys()

        sprite_collided = collide_fn(group, dokill, collided)
        if sprite_collided is not None:
            self.move_x_back_if_collided(sprite_collided)
            self.velocity.x = 0
        else:
            self.acceleration.x += self.velocity.x * self.friction.x
            self.velocity.x += self.acceleration.x

        self.set_new_position_x()

    def move_y_with_collision(self, collide_fn, group, dokill=None, collided=None):
        self.acceleration.y = self.start_of_new_frame_acceleration.y
        self.apply_acceleration_y_using_pressed_keys()

        sprite_collided = collide_fn(group, dokill, collided)
        if sprite_collided is not None:
            self.move_y_back_if_collided(sprite_collided)
            if sprite_collided["side"] == "top":
                self.velocity.y *= self.after_bounce_velocity_ratio
            elif sprite_collided["side"] == "bottom":
                self.velocity.y = 0
                self.jump_if_key_pressed()
        else:
            self.acceleration.y += self.velocity.y * self.friction.y
            self.velocity.y += self.acceleration.y

        self.set_new_position_y()


    def apply_acceleration_x_using_pressed_keys(self):
        pressed_keys = pygame.key.get_pressed()

        if self._keybinds.is_key_pressed_for_option("left", pressed_keys):
            self.acceleration.x -= self._keybinds.get_value_for_option("left")
        if self._keybinds.is_key_pressed_for_option("right", pressed_keys):
            self.acceleration.x += self._keybinds.get_value_for_option("right")

    def apply_acceleration_y_using_pressed_keys(self):
        pressed_keys = pygame.key.get_pressed()

        if self._keybinds.is_key_pressed_for_option("up", pressed_keys):
            self.acceleration.y -= self._keybinds.get_value_for_option("up")
        if self._keybinds.is_key_pressed_for_option("down", pressed_keys):
            self.acceleration.y += self._keybinds.get_value_for_option("down")

    def set_new_position_x(self):
        self.position = self.position.move(self.velocity.x + (0.5 * self.acceleration.x), 0)
        if self.should_wrap_screen_x:
            self.wrap_around_screen_x()
        self.rect.x = self.position.x

    def set_new_position_y(self):
        self.position = self.position.move(0, self.velocity.y + (0.5 * self.acceleration.y))
        if self.should_wrap_screen_y:
            self.wrap_around_screen_y()
        self.rect.y = self.position.y

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

    def jump_if_key_pressed(self):
        if self._keybinds.is_key_pressed_for_option("jump"):
            self.velocity.y = -self._keybinds.get_value_for_option("jump")
        
    def move_x_back_if_collided(self, sprite_collided):
        if sprite_collided is not None:
            if sprite_collided["side"] == "right":
                self.position.right = sprite_collided["sprite"].rect.left
            if sprite_collided["side"] == "left":
                self.position.left = sprite_collided["sprite"].rect.right

    def move_y_back_if_collided(self, sprite_collided):
        if sprite_collided is not None:
            if sprite_collided["side"] == "bottom":
                self.position.bottom = sprite_collided["sprite"].rect.top
            if sprite_collided["side"] == "top":
                self.position.top = sprite_collided["sprite"].rect.bottom

    def get_x_collision(self, group, dokill=False, collided=None):
        sprite_collided = self.get_collision_right(group, dokill, collided)
        if sprite_collided is not None:
            return sprite_collided
        else:
            return self.get_collision_left(group, dokill, collided)


    def get_collision_right(self, group, dokill=False, collided=None):
        if self.velocity.x > 0 or (self.velocity.x == 0 and self.acceleration.x > 0):
            self.rect.x += 1
            sprites_collided = pygame.sprite.spritecollide(self.parent, group, dokill, collided)
            self.rect.x -= 1

            for sprite in sprites_collided:
                if abs(self.position.right - sprite.rect.left) < self.collision_tolerance_x:
                    return {"sprite": sprite, "side": "right"}
        return None

    def get_collision_left(self, group, dokill=False, collided=None):
        if self.velocity.x < 0 or (self.velocity.x == 0 and self.acceleration.x < 0):
            self.rect.x -= 1
            sprites_collided = pygame.sprite.spritecollide(self.parent, group, dokill, collided)
            self.rect.x += 1

            for sprite in sprites_collided:
                if abs(self.position.left - sprite.rect.right) < self.collision_tolerance_x:
                    return {"sprite": sprite, "side": "left"}
        return None
        
    def get_y_collision(self, group, dokill=False, collided=None):
        sprite_collided = self.get_collision_bottom(group, dokill, collided)
        if sprite_collided is not None:
            return sprite_collided
        else:
            return self.get_collision_top(group, dokill, collided)

    def get_collision_bottom(self, group, dokill=False, collided=None):
        if self.velocity.y > 0 or (self.velocity.y == 0 and self.acceleration.y > 0):
            self.rect.y += 1
            sprites_collided = pygame.sprite.spritecollide(self.parent, group, dokill, collided)
            self.rect.y -= 1

            for sprite in sprites_collided:
                if abs(self.position.bottom - sprite.rect.top) < self.collision_tolerance_y:
                    return {"sprite": sprite, "side": "bottom"}
        return None

    def get_collision_top(self, group, dokill=False, collided=None):
        if self.velocity.y < 0 or (self.velocity.y == 0 and self.acceleration.y < 0):
            self.rect.y -= 1
            sprites_collided = pygame.sprite.spritecollide(self.parent, group, dokill, collided)
            self.rect.y += 1

            for sprite in sprites_collided:
                if abs(self.position.top - sprite.rect.bottom) < self.collision_tolerance_y:
                    return {"sprite": sprite, "side": "top"}
        return None

    @property
    def collision_tolerance_x(self):
        return abs(self.velocity.x + (0.5 * self.acceleration.x)) * 2

    @property
    def collision_tolerance_y(self):
        return abs(self.velocity.y + (0.5 * self.acceleration.y)) * 2

    def spritecollide(self, group):
        return [sprite for sprite in group if self.position.colliderect(sprite.rect)]