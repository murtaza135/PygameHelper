import pygame
from movement_component import MovementComponent
from rotator2 import Rotator2


class AccelerationMovementComponent(MovementComponent):

    def __init__(self, parent, rect, constant_acceleration_delta, friction, default_position=(0, 0), 
                default_rotation=Rotator2.RIGHT, default_velocity=(0, 0), default_acceleration=(0, 0),
                window_size=(800, 600), after_bounce_velocity_ratios=(0, 0, 0, 0), should_wrap_screen=(True, True)):

        super().__init__(parent, rect, constant_acceleration_delta, friction, default_position=default_position, 
                        default_rotation=default_rotation, default_velocity=default_velocity, default_acceleration=default_acceleration,
                        window_size=window_size, after_bounce_velocity_ratios=after_bounce_velocity_ratios, should_wrap_screen=should_wrap_screen)

        self.key_pressed_order = list()

    # def process_input(self):
    #     pressed_keys = pygame.key.get_pressed()

    #     if self.keybinds.is_key_pressed_for_option("left", pressed_keys):
    #         self.constant_acceleration_delta.x = -abs(self.default_acceleration.x)
    #         self.constant_acceleration_delta.y = 0
    #         self.velocity.y = 0
    #     elif self.keybinds.is_key_pressed_for_option("right", pressed_keys):
    #         self.constant_acceleration_delta.x = abs(self.default_acceleration.x)
    #         self.constant_acceleration_delta.y = 0
    #         self.velocity.y = 0
    #     elif self.keybinds.is_key_pressed_for_option("up", pressed_keys):
    #         self.constant_acceleration_delta.y = -abs(self.default_acceleration.y)
    #         self.constant_acceleration_delta.x = 0
    #         self.velocity.x = 0
    #     elif self.keybinds.is_key_pressed_for_option("down", pressed_keys):
    #         self.constant_acceleration_delta.y = abs(self.default_acceleration.y)
    #         self.constant_acceleration_delta.x = 0
    #         self.velocity.x = 0
            
    def process_input(self):
        pressed_keys = pygame.key.get_pressed()

        for key in [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE]:
            if pressed_keys[key]:
                if key not in self.key_pressed_order:
                    self.key_pressed_order.append(key)
            else:
                try:
                    self.key_pressed_order.remove(key)
                except ValueError:
                    pass

        if len(self.key_pressed_order) != 0:
            if self.key_pressed_order[-1] == pygame.K_a:
                self.acceleration.x -= self.keybinds.get_value_for_option("left")
                self.velocity.y = 0
            if self.key_pressed_order[-1] == pygame.K_d:
                self.acceleration.x += self.keybinds.get_value_for_option("right")
                self.velocity.y = 0
            if self.key_pressed_order[-1] == pygame.K_w:
                self.acceleration.y -= self.keybinds.get_value_for_option("up")
                self.velocity.x = 0
            if self.key_pressed_order[-1] == pygame.K_s:
                self.acceleration.y += self.keybinds.get_value_for_option("down")
                self.velocity.x = 0


        # if self.keybinds.is_key_pressed_for_option("left", pressed_keys):
        #     self.acceleration.x -= self.keybinds.get_value_for_option("left")
        #     self.velocity.y = 0
        # elif self.keybinds.is_key_pressed_for_option("right", pressed_keys):
        #     self.acceleration.x += self.keybinds.get_value_for_option("right")
        #     self.velocity.y = 0
        # elif self.keybinds.is_key_pressed_for_option("up", pressed_keys):
        #     self.acceleration.y -= self.keybinds.get_value_for_option("up")
        #     self.velocity.x = 0
        # elif self.keybinds.is_key_pressed_for_option("down", pressed_keys):
        #     self.acceleration.y += self.keybinds.get_value_for_option("down")
        #     self.velocity.x = 0

    def process_input_for_x(self):
        pressed_keys = pygame.key.get_pressed()

        if self.keybinds.is_key_pressed_for_option("left", pressed_keys):
            self.acceleration.x -= self.keybinds.get_value_for_option("left")
        if self.keybinds.is_key_pressed_for_option("right", pressed_keys):
            self.acceleration.x += self.keybinds.get_value_for_option("right")

    def process_input_for_y(self):
        pressed_keys = pygame.key.get_pressed()

        if self.keybinds.is_key_pressed_for_option("up", pressed_keys):
            self.acceleration.y -= self.keybinds.get_value_for_option("up")
        if self.keybinds.is_key_pressed_for_option("down", pressed_keys):
            self.acceleration.y += self.keybinds.get_value_for_option("down")

    def jump_if_key_pressed(self):
        if self.keybinds.is_key_pressed_for_option("jump"):
            self.velocity.y = -self.keybinds.get_value_for_option("jump")