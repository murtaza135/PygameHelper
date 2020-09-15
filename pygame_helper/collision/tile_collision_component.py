import pygame
from pygame_helper.collision.abstract_collision_component import AbstractCollisionComponent


class TileCollisionComponent(AbstractCollisionComponent):

    def __init__(self, movement_component):
        super().__init__(movement_component)
        self.tile_geometry = self.movement.tile_geometry

    def get_collision_right(self, group, dokill=False, collide_callback=None):
        if self.movement.velocity.x > 0:
            self.movement.rect.x += self.tile_geometry.width
            sprites_collided = pygame.sprite.spritecollide(self.parent_sprite, group, dokill, collide_callback)
            self.movement.rect.x -= self.tile_geometry.width
            if sprites_collided:
                return {"sprite": sprites_collided[0], "side": "right"}
        return None

    def get_collision_left(self, group, dokill=False, collide_callback=None):
        if self.movement.velocity.x < 0:
            self.movement.rect.x -= self.tile_geometry.width
            sprites_collided = pygame.sprite.spritecollide(self.parent_sprite, group, dokill, collide_callback)
            self.movement.rect.x += self.tile_geometry.width
            if sprites_collided:
                return {"sprite": sprites_collided[0], "side": "left"}
        return None
        
    def get_collision_bottom(self, group, dokill=False, collide_callback=None):
        if self.movement.velocity.y > 0:
            self.movement.rect.y += self.tile_geometry.height
            sprites_collided = pygame.sprite.spritecollide(self.parent_sprite, group, dokill, collide_callback)
            self.movement.rect.y -= self.tile_geometry.height
            if sprites_collided:
                return {"sprite": sprites_collided[0], "side": "bottom"}
        return None

    def get_collision_top(self, group, dokill=False, collide_callback=None):
        if self.movement.velocity.y < 0:
            self.movement.rect.y -= self.tile_geometry.height
            sprites_collided = pygame.sprite.spritecollide(self.parent_sprite, group, dokill, collide_callback)
            self.movement.rect.y += self.tile_geometry.height
            if sprites_collided:
                return {"sprite": sprites_collided[0], "side": "top"}
        return None