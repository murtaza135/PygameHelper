import pygame
from pygame_helper.abstract_collision_component import AbstractCollisionComponent


class AccelerationCollisionComponent(AbstractCollisionComponent):
    
    def __init__(self, movement_component):
        super().__init__(movement_component)

    def get_collision_right(self, group, dokill=False, collide_callback=None):
        if collide_callback == None:
            collide_callback = AbstractCollisionComponent.collide_positional_rect

        if self.movement.velocity.x > 0 or (self.movement.velocity.x == 0 and self.movement.acceleration.x > 0):
            sprites_collided = pygame.sprite.spritecollide(self.parent_sprite, group, dokill, collide_callback)
            if sprites_collided:
                return {"sprite": sprites_collided[0], "side": "right"}
        return None

    def get_collision_left(self, group, dokill=False, collide_callback=None):
        if collide_callback == None:
            collide_callback = AbstractCollisionComponent.collide_positional_rect

        if self.movement.velocity.x < 0 or (self.movement.velocity.x == 0 and self.movement.acceleration.x < 0):
            sprites_collided = pygame.sprite.spritecollide(self.parent_sprite, group, dokill, collide_callback)
            if sprites_collided:
                return {"sprite": sprites_collided[0], "side": "left"}
        return None
        
    def get_collision_bottom(self, group, dokill=False, collide_callback=None):
        if collide_callback == None:
            collide_callback = AbstractCollisionComponent.collide_positional_rect

        if self.movement.velocity.y > 0 or (self.movement.velocity.y == 0 and self.movement.acceleration.y > 0):
            sprites_collided = pygame.sprite.spritecollide(self.parent_sprite, group, dokill, collide_callback)
            if sprites_collided:
                return {"sprite": sprites_collided[0], "side": "bottom"}
        return None

    def get_collision_top(self, group, dokill=False, collide_callback=None):
        if collide_callback == None:
            collide_callback = AbstractCollisionComponent.collide_positional_rect

        if self.movement.velocity.y < 0 or (self.movement.velocity.y == 0 and self.movement.acceleration.y < 0):
            sprites_collided = pygame.sprite.spritecollide(self.parent_sprite, group, dokill, collide_callback)
            if sprites_collided:
                return {"sprite": sprites_collided[0], "side": "top"}
        return None