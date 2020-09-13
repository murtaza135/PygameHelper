import pygame
from collision_component import CollisionComponent


class TileCollisionComponent(CollisionComponent):

    def __init__(self, movement_component):
        self.movement = movement_component
        self.parent_sprite = self.movement.parent
        self.tile_geometry = self.movement.tile_geometry

    def get_x_collision(self, group, dokill=False, collide_callback=None):
        sprite_collided = self.get_collision_right(group, dokill, collide_callback)
        if sprite_collided is not None:
            return sprite_collided
        else:
            return self.get_collision_left(group, dokill, collide_callback)

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
        
    def get_y_collision(self, group, dokill=False, collide_callback=None):
        sprite_collided = self.get_collision_bottom(group, dokill, collide_callback)
        if sprite_collided is not None:
            return sprite_collided
        else:
            return self.get_collision_top(group, dokill, collide_callback)

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

    @staticmethod
    def collide_positional_rect(sprite_one, sprite_two):
        return sprite_one.movement.position.rect.colliderect(sprite_two.rect)