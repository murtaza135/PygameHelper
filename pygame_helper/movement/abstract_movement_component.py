from abc import ABC, abstractmethod


class AbstractMovementComponent(ABC):

    ### movement_type ###
    FOUR_WAY_MOVEMENT = "four_way_movement"
    EIGHT_WAY_MOVEMENT = "eight_way_movement"
    ROTATIONAL_MOVEMENT = "rotational_movement"

    ### direction_control ###
    DIRECTION_ONLY = "direction_only"
    DIRECTION_AND_MAGNITUDE = "direction_and_magnitude"

    
    def __init__(self, game_mode, parent_sprite, rect):
        self.game_mode = game_mode
        self.parent_sprite = parent_sprite
        self.rect = rect

    @property
    def frametime(self):
        try:
            frametime_ms = self.game_mode.game.clock.get_time()
        except AttributeError:
            frametime_ms = self.game_mode.clock.get_time()
        frametime_seconds = frametime_ms / 1000
        return frametime_seconds

    def check_direction_control_y_for_eight_way_movement(self):
        if self.movement_type == AbstractMovementComponent.EIGHT_WAY_MOVEMENT:
            if self.direction_control_y is None:
                raise ValueError("direction_control_y cannot be None if Eight Way Movement is used")


    @abstractmethod
    def move(self):
        pass

    def move_with_collision(self, collide_fn_x, collide_fn_y, group, dokill=None, collide_callback=None):
        raise NotImplementedError


    @abstractmethod
    def _process_movement_input(self):
        pass

    
    @staticmethod
    def collide_positional_rect(sprite_one, sprite_two):
        return sprite_one.movement.position.rect.colliderect(sprite_two.rect)

    @staticmethod
    def collide_positional_rect_if_possible(sprite_one, sprite_two):
        try:
            return sprite_one.movement.position.rect.colliderect(sprite_two.rect)
        except AttributeError:
            return sprite_one.rect.colliderect(sprite_two.rect)