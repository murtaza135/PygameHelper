import pygame
from movement_component import MovementComponent
from rotator2 import Rotator2
from utilities import WHTuple, XYTuple, NESWTuple


class DirectionMovementComponent(MovementComponent):

    def __init__(self, parent, rect, constant_acceleration_delta, friction, default_position=(0, 0), 
                default_rotation=Rotator2.RIGHT, default_velocity=(0, 0), default_acceleration=(0, 0),
                window_size=(800, 600), after_bounce_velocity_ratios=(0, 0, 0, 0), should_wrap_screen=(True, True),
                should_use_direction=(True, True)):

        super().__init__(parent, rect, constant_acceleration_delta, friction, default_position=default_position, 
                        default_rotation=default_rotation, default_velocity=default_velocity, default_acceleration=default_acceleration,
                        window_size=window_size, after_bounce_velocity_ratios=after_bounce_velocity_ratios, should_wrap_screen=should_wrap_screen)

        self.should_use_direction = XYTuple(*should_use_direction)

    def process_input(self):
        pass

    def process_input_for_x(self):
        pressed_keys = pygame.key.get_pressed()

        if self.keybinds.is_key_pressed_for_option("left", pressed_keys):
            self.constant_acceleration_delta.x = abs(self.constant_acceleration_delta.x) * (-1)
        elif self.keybinds.is_key_pressed_for_option("right", pressed_keys):
            self.constant_acceleration_delta.x = abs(self.constant_acceleration_delta.x)
        self.acceleration.x = self.constant_acceleration_delta.x

    def process_input_for_y(self):
        pressed_keys = pygame.key.get_pressed()

        if self.keybinds.is_key_pressed_for_option("up", pressed_keys):
            self.constant_acceleration_delta.y = abs(self.constant_acceleration_delta.y) * (-1)
        elif self.keybinds.is_key_pressed_for_option("down", pressed_keys):
            self.constant_acceleration_delta.y = abs(self.constant_acceleration_delta.y)
        self.acceleration.y = self.constant_acceleration_delta.y

    def jump_if_key_pressed(self):
        if self.keybinds.is_key_pressed_for_option("jump"):
            self.velocity.y = -self.keybinds.get_value_for_option("jump")