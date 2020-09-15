import pygame
from pygame_helper.abstract_input_component import AbstractInputComponent 


class AccelerationInputComponent(AbstractInputComponent):

    def __init__(self, movement_component, keybinder, movement_type, direction_control, direction_control_y=None):
        super().__init__(movement_component, keybinder, movement_type, direction_control, direction_control_y)

    def set_jump_velocity_leftwards_if_key_pressed(self):
        if self.keybinder.is_key_pressed_for_option("jump"):
            self.movement.velocity.x = -abs(self.keybinder.get_value_for_option("jump"))

    def set_jump_velocity_rightwards_if_key_pressed(self):
        if self.keybinder.is_key_pressed_for_option("jump"):
            self.movement.velocity.x = abs(self.keybinder.get_value_for_option("jump"))

    def set_jump_velocity_upwards_if_key_pressed(self):
        if self.keybinder.is_key_pressed_for_option("jump"):
            self.movement.velocity.y = -abs(self.keybinder.get_value_for_option("jump"))

    def set_jump_velocity_downwards_if_key_pressed(self):
        if self.keybinder.is_key_pressed_for_option("jump"):
            self.movement.velocity.y = abs(self.keybinder.get_value_for_option("jump"))

    def process_movement_input(self):
        if self.movement_type == AbstractInputComponent.ROTATIONAL_MOVEMENT:
            if self.direction_control == AbstractInputComponent.DIRECTION_AND_MAGNITUDE:
                self._apply_rotation_and_acceleration()
            elif self.direction_control == AbstractInputComponent.DIRECTION_ONLY:
                self._apply_rotation_only()
            self._rotate_image_and_rect_at_center()

        elif self.movement_type == AbstractInputComponent.FOUR_WAY_MOVEMENT:
            if self.direction_control == AbstractInputComponent.DIRECTION_AND_MAGNITUDE:
                self._apply_acceleration_in_one_direction_only()
            elif self.direction_control == AbstractInputComponent.DIRECTION_ONLY:
                self._change_absolute_direction()

        elif self.movement_type == AbstractInputComponent.EIGHT_WAY_MOVEMENT:
            if self.direction_control == AbstractInputComponent.DIRECTION_AND_MAGNITUDE:
                self._apply_acceleration_x()
            elif self.direction_control == AbstractInputComponent.DIRECTION_ONLY:
                self._change_direction_x()

            if self.direction_control_y == AbstractInputComponent.DIRECTION_AND_MAGNITUDE:
                self._apply_acceleration_y()
            elif self.direction_control_y == AbstractInputComponent.DIRECTION_ONLY:
                self._change_direction_y()

    def _apply_rotation_and_acceleration(self):
        if self.keybinder.is_key_pressed_for_option("left"):
            self.movement.rotation.rotator -= self.keybinder.get_value_for_option("left") * self.movement.frametime
        if self.keybinder.is_key_pressed_for_option("right"):
            self.movement.rotation.rotator += self.keybinder.get_value_for_option("right") * self.movement.frametime
        if self.keybinder.is_key_pressed_for_option("up"):
            self.movement.acceleration.x += self.keybinder.get_value_for_option("up")
            self.movement.acceleration = self.movement.acceleration.rotate(self.movement.rotation.rotator)
        if self.keybinder.is_key_pressed_for_option("down"):
            self.movement.acceleration.x -= self.keybinder.get_value_for_option("down")
            self.movement.acceleration = self.movement.acceleration.rotate(self.movement.rotation.rotator)

    def _apply_rotation_only(self):
        if self.keybinder.is_key_pressed_for_option("left"):
            self.movement.rotation.rotator -= self.keybinder.get_value_for_option("left") * self.movement.frametime
        if self.keybinder.is_key_pressed_for_option("right"):
            self.movement.rotation.rotator += self.keybinder.get_value_for_option("right") * self.movement.frametime
        self.movement.acceleration = self.movement.acceleration.rotate(self.movement.rotation.rotator)

    def _rotate_image_and_rect_at_center(self):
        self.parent_sprite.image = pygame.transform.rotate(
            self.parent_sprite.original_image,
            -self.movement.rotation.rotator
        )
        self.parent_sprite.rect = self.parent_sprite.image.get_rect()
        self.movement.rect = self.parent_sprite.rect
        self.movement.rect.centerx = self.movement.position.centerx
        self.movement.rect.centery = self.movement.position.centery

    def _apply_acceleration_in_one_direction_only(self):
        self.keybinder.track_keys_for_multiple_options("right", "left", "up", "down")
        self.keybinder.update_pressed_keys_order()

        if self.keybinder.is_key_most_recently_pressed_for_option("left"):
            self.movement.acceleration.x -= self.keybinder.get_value_for_option("left")
            self.movement.velocity.y = 0
        if self.keybinder.is_key_most_recently_pressed_for_option("right"):
            self.movement.acceleration.x += self.keybinder.get_value_for_option("right")
            self.movement.velocity.y = 0
        if self.keybinder.is_key_most_recently_pressed_for_option("up"):
            self.movement.acceleration.y -= self.keybinder.get_value_for_option("up")
            self.movement.velocity.x = 0
        if self.keybinder.is_key_most_recently_pressed_for_option("down"):
            self.movement.acceleration.y += self.keybinder.get_value_for_option("down")
            self.movement.velocity.x = 0

    def _change_absolute_direction(self):
        if self.keybinder.is_key_pressed_for_option("left"):
            self.movement.constant_acceleration_delta.x = -abs(self.movement.default_acceleration_delta.x)
            self.movement.constant_acceleration_delta.y = 0
            self.movement.velocity.y = 0
        elif self.keybinder.is_key_pressed_for_option("right"):
            self.movement.constant_acceleration_delta.x = abs(self.movement.default_acceleration_delta.x)
            self.movement.constant_acceleration_delta.y = 0
            self.movement.velocity.y = 0
        elif self.keybinder.is_key_pressed_for_option("up"):
            self.movement.constant_acceleration_delta.x = 0
            self.movement.constant_acceleration_delta.y = -abs(self.movement.default_acceleration_delta.y)
            self.movement.velocity.x = 0
        elif self.keybinder.is_key_pressed_for_option("down"):
            self.movement.constant_acceleration_delta.x = 0
            self.movement.constant_acceleration_delta.y = abs(self.movement.default_acceleration_delta.y)
            self.movement.velocity.x = 0
        
        self.movement.acceleration.x = self.movement.constant_acceleration_delta.x
        self.movement.acceleration.y = self.movement.constant_acceleration_delta.y

    def _apply_acceleration_x(self):
        if self.keybinder.is_key_pressed_for_option("left"):
            self.movement.acceleration.x -= self.keybinder.get_value_for_option("left")
        if self.keybinder.is_key_pressed_for_option("right"):
            self.movement.acceleration.x += self.keybinder.get_value_for_option("right")

    def _change_direction_x(self):
        if self.keybinder.is_key_pressed_for_option("left"):
            self.movement.constant_acceleration_delta.x = -abs(self.movement.constant_acceleration_delta.x)
        elif self.keybinder.is_key_pressed_for_option("right"):
            self.movement.constant_acceleration_delta.x = abs(self.movement.constant_acceleration_delta.x)
        self.movement.acceleration.x = self.movement.constant_acceleration_delta.x

    def _apply_acceleration_y(self):
        if self.keybinder.is_key_pressed_for_option("up"):
            self.movement.acceleration.y -= self.keybinder.get_value_for_option("up")
        if self.keybinder.is_key_pressed_for_option("down"):
            self.movement.acceleration.y += self.keybinder.get_value_for_option("down")

    def _change_direction_y(self):
        if self.keybinder.is_key_pressed_for_option("up"):
            self.movement.constant_acceleration_delta.y = -abs(self.movement.constant_acceleration_delta.y)
        elif self.keybinder.is_key_pressed_for_option("down"):
            self.movement.constant_acceleration_delta.y = abs(self.movement.constant_acceleration_delta.y)
        self.movement.acceleration.y = self.movement.constant_acceleration_delta.y