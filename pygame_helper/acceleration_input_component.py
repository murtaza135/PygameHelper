import pygame
from input_component import InputComponent 


class AccelerationInputComponent(InputComponent):

    ### movement_type ###
    FOUR_WAY_MOVEMENT = "four_way_movement"
    EIGHT_WAY_MOVEMENT = "eight_way_movement"
    ROTATIONAL_MOVEMENT = "rotational_movement"

    ### direction_control ###
    DIRECTION_ONLY = "direction_only"
    DIRECTION_AND_MAGNITUDE = "direction_and_magnitude"
    
    
    def __init__(self, movement_component, keybinder, movement_type, direction_control, direction_control_y=None):
        self.movement = movement_component
        self.parent_sprite = self.movement.parent
        self.keybinder = keybinder

        self.movement_type = movement_type
        self.direction_control = direction_control
        self.direction_control_y = direction_control_y

        self._check_direction_control_y_for_eight_way_movement()

    def _check_direction_control_y_for_eight_way_movement(self):
        if self.movement_type == AccelerationInputComponent.EIGHT_WAY_MOVEMENT:
            if self.direction_control_y is None:
                raise ValueError("direction_control_y cannot be None if Eight Way Movement is used")


    def set_jump_velocity_if_key_pressed(self):
        if self.keybinder.is_key_pressed_for_option("jump"):
            self.movement.velocity.y = -abs(self.keybinder.get_value_for_option("jump"))

    def process_movement_input(self):
        if self.movement_type == AccelerationInputComponent.ROTATIONAL_MOVEMENT:
            if self.direction_control == AccelerationInputComponent.DIRECTION_AND_MAGNITUDE:
                self._apply_rotation_and_acceleration()
            elif self.direction_control == AccelerationInputComponent.DIRECTION_ONLY:
                self._apply_rotation_only()
            self._rotate_image_and_rect_at_center()

        elif self.movement_type == AccelerationInputComponent.FOUR_WAY_MOVEMENT:
            if self.direction_control == AccelerationInputComponent.DIRECTION_AND_MAGNITUDE:
                self._apply_acceleration_in_one_direction_only()
            elif self.direction_control == AccelerationInputComponent.DIRECTION_ONLY:
                self._change_absolute_direction()

        elif self.movement_type == AccelerationInputComponent.EIGHT_WAY_MOVEMENT:
            if self.direction_control == AccelerationInputComponent.DIRECTION_AND_MAGNITUDE:
                self._apply_acceleration_x()
            elif self.direction_control == AccelerationInputComponent.DIRECTION_ONLY:
                self._change_direction_x()

            if self.direction_control_y == AccelerationInputComponent.DIRECTION_AND_MAGNITUDE:
                self._apply_acceleration_y()
            elif self.direction_control_y == AccelerationInputComponent.DIRECTION_ONLY:
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