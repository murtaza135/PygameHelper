from abc import ABC, abstractmethod


class AbstractCollisionComponent(ABC):
    
    def __init__(self, movement_component):
        self.movement = movement_component
        self.parent_sprite = self.movement.parent

    def get_x_collision(self, group, dokill=False, collide_callback=None):
        sprite_collided = self.get_collision_right(group, dokill, collide_callback)
        if sprite_collided is not None:
            return sprite_collided
        else:
            return self.get_collision_left(group, dokill, collide_callback)

    @abstractmethod
    def get_collision_right(self, group, dokill=False, collide_callback=None):
        pass

    @abstractmethod
    def get_collision_left(self, group, dokill=False, collide_callback=None):
        pass

    def get_y_collision(self, group, dokill=False, collide_callback=None):
        sprite_collided = self.get_collision_bottom(group, dokill, collide_callback)
        if sprite_collided is not None:
            return sprite_collided
        else:
            return self.get_collision_top(group, dokill, collide_callback)

    @abstractmethod
    def get_collision_bottom(self, group, dokill=False, collide_callback=None):
        pass

    @abstractmethod
    def get_collision_top(self, group, dokill=False, collide_callback=None):
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