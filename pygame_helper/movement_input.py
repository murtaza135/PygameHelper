import pygame
from utilities import WHTuple, XYTuple, NESWTuple


class MovementInput(object):

    MAGNITUDE = "magnitude"
    DIRECTION = "direction"
    OPPOSITE_DIRECTION = "opposite_direction"
    ABSOLUTE_DIRECTION = "absolute_direction"

    def __init__(self, movement_component, movement_type, should_use_8_way_movement=True):
        self.movement_component = movement_component
        self.movement_type = XYTuple(*movement_type)
        self.should_use_8_way_movement = should_use_8_way_movement

        self.keybinds = self.movement_component.keybinds
        self.magnitude_value = self.movement_component.acceleration

    # def _set_movement_type_based_upon_8_way_movement(self, movement_type):
    #     if not self.should_use_8_way_movement:
    #         self.movement_type = XYTuple(movement_type[0], movement_type[0])
    #     else:
    #         self.movement_type = XYTuple(*movement_type)

    def process_input(self):
        # if self.movement_type.x == MovementInput.ABSOLUTE_DIRECTION or self.movement_type.x == MovementInput.ABSOLUTE_DIRECTION:
        #     self.change_to_absolute_direction()
        # else:
        #     if self.movement_type.x == MovementInput.ABSOLUTE_DIRECTION:
        #         pass

        if not self.should_use_8_way_movement:
            if self.movement_type.x == MovementInput.MAGNITUDE:
                self.apply_magnitude_value_in_one_direction_only()
            elif self.movement_type.x == MovementInput.DIRECTION:
                self.change_absolute_direction()
        else:
            if self.movement_type.x == MovementInput.MAGNITUDE:
                self.apply_magnitude_x()
            elif self.movement_type.x == MovementInput.DIRECTION:
                self.change_direction_x()

            if self.movement_type.y == MovementInput.MAGNITUDE:
                self.apply_magnitude_y()
            elif self.movement_type.y == MovementInput.DIRECTION:
                self.change_direction_y()

    def apply_magnitude_value_in_one_direction_only(self):
        pressed_keys = pygame.key.get_pressed()

        if self.keybinds.is_key_pressed_for_option("left", pressed_keys):
            self.acceleration.x -= self.keybinds.get_value_for_option("left")
        elif self.keybinds.is_key_pressed_for_option("right", pressed_keys):
            self.acceleration.x += self.keybinds.get_value_for_option("right")
        elif self.keybinds.is_key_pressed_for_option("up", pressed_keys):
            self.acceleration.y -= self.keybinds.get_value_for_option("up")
        elif self.keybinds.is_key_pressed_for_option("down", pressed_keys):
            self.acceleration.y += self.keybinds.get_value_for_option("down")

    def change_absolute_direction(self):
        pressed_keys = pygame.key.get_pressed()

        if self.keybinds.is_key_pressed_for_option("left", pressed_keys):
            self.constant_acceleration_delta.x = -abs(self.default_acceleration.x)
            self.constant_acceleration_delta.y = 0
            self.velocity.y = 0
        elif self.keybinds.is_key_pressed_for_option("right", pressed_keys):
            self.constant_acceleration_delta.x = abs(self.default_acceleration.x)
            self.constant_acceleration_delta.y = 0
            self.velocity.y = 0
        elif self.keybinds.is_key_pressed_for_option("up", pressed_keys):
            self.constant_acceleration_delta.y = -abs(self.default_acceleration.y)
            self.constant_acceleration_delta.x = 0
            self.velocity.x = 0
        elif self.keybinds.is_key_pressed_for_option("down", pressed_keys):
            self.constant_acceleration_delta.y = abs(self.default_acceleration.y)
            self.constant_acceleration_delta.x = 0
            self.velocity.x = 0

        self.acceleration.x = self.constant_acceleration_delta.x
        self.acceleration.y = self.constant_acceleration_delta.y