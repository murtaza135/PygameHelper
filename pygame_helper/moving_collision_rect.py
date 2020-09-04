import pygame
from multipledispatch import dispatch


class MovingCollisionRect(pygame.Rect):
    
    @dispatch(object, object, object, object, object)
    def __init__(self, parent, x, y, width, height):
        super().__init__(x, y, width, height)
        self.initialise_collision_rect(parent)

    @dispatch(object, tuple, tuple)
    def __init__(self, parent, coords, dimensions):
        super().__init__(coords, dimensions)
        self.initialise_collision_rect(parent)

    @dispatch(object, pygame.Rect)
    def __init__(self, parent, rect):
        super().__init__(rect)
        self.initialise_collision_rect(parent)

    def initialise_collision_rect(self, parent):
        self.parent = parent
        self.left_colliding = False
        self.right_colliding = False
        self.top_colliding = False
        self.bottom_colliding = False

    def reset_horizontal_colliding_sides(self):
        self.left_colliding = False
        self.right_colliding = False
    
    def reset_vertical_colliding_sides(self):
        self.top_colliding = False
        self.bottom_colliding = False

    def move_x_back_if_colliding(self, group):
        self.reset_horizontal_colliding_sides()

        for sprite in group:
            if self.parent.movement.velocity.x > 0:
                self.right = sprite.rect.left
                self.right_colliding = True
            elif self.parent.movement.velocity.x < 0:
                self.left = sprite.rect.right
                self.left_colliding = True
    
    def move_y_back_if_colliding(self, group):
        self.reset_vertical_colliding_sides()

        for sprite in group:
            if self.parent.movement.velocity.y > 0:
                self.bottom = sprite.rect.top + 1
                self.bottom_colliding = True
            elif self.parent.movement.velocity.y < 0:
                self.top = sprite.rect.bottom
                self.top_colliding = True