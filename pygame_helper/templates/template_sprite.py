import pygame
from pygame_helper import MovingCollisionRect
# from pygame_helper import MovementComponent
# from pygame_helper import AnimationComponent


class TemplateSprite(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.image = None
        self.rect = MovingCollisionRect(self.image.get_rect())
        # self.movement = MovementComponent()
        # self.animation = AnimationComponent()

    def update(self):
        pass

    def render(self, window):
        pass