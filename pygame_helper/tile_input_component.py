import pygame
from input_component import InputComponent


class TileInputComponent(InputComponent):

    ### movement_type ###
    FOUR_WAY_MOVEMENT = "four_way_movement"
    EIGHT_WAY_MOVEMENT = "eight_way_movement"

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
        if self.movement_type == TileInputComponent.EIGHT_WAY_MOVEMENT:
            if self.direction_control_y is None:
                raise ValueError("direction_control_y cannot be None if Eight Way Movement is used")