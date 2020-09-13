import pygame
from collision_component import CollisionComponent


class VelocityCollisionComponent(CollisionComponent):
    
    def __init__(self, movement_component):
        self.movement = movement_component
        self.parent_sprite = self.movement.parent

    def get_x_collision(self, group, dokill=False, collide_callback=None):
        sprite_collided = self.get_collision_right(group, dokill, collide_callback)
        if sprite_collided is not None:
            return sprite_collided
        else:
            return self.get_collision_left(group, dokill, collide_callback)

    def get_collision_right(self, group, dokill=False, collide_callback=None):
        if collide_callback == None:
            collide_callback = VelocityCollisionComponent.collide_positional_rect

        if self.movement.velocity.x > 0:
            sprites_collided = pygame.sprite.spritecollide(self.parent_sprite, group, dokill, collide_callback)
            if sprites_collided:
                return {"sprite": sprites_collided[0], "side": "right"}
        return None

    def get_collision_left(self, group, dokill=False, collide_callback=None):
        if collide_callback == None:
            collide_callback = VelocityCollisionComponent.collide_positional_rect

        if self.movement.velocity.x < 0:
            sprites_collided = pygame.sprite.spritecollide(self.parent_sprite, group, dokill, collide_callback)
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
        if collide_callback == None:
            collide_callback = VelocityCollisionComponent.collide_positional_rect

        if self.movement.velocity.y > 0:
            sprites_collided = pygame.sprite.spritecollide(self.parent_sprite, group, dokill, collide_callback)
            if sprites_collided:
                return {"sprite": sprites_collided[0], "side": "bottom"}
        return None

    def get_collision_top(self, group, dokill=False, collide_callback=None):
        if collide_callback == None:
            collide_callback = VelocityCollisionComponent.collide_positional_rect

        if self.movement.velocity.y < 0:
            sprites_collided = pygame.sprite.spritecollide(self.parent_sprite, group, dokill, collide_callback)
            if sprites_collided:
                return {"sprite": sprites_collided[0], "side": "top"}
        return None

    @staticmethod
    def collide_positional_rect(sprite_one, sprite_two):
        return sprite_one.movement.position.rect.colliderect(sprite_two.rect)