import pygame
from base_widget import Widget


class ImageWidget(Widget):

    def __init__(self, image_path, geometry=None, action=None):
        super().__init__(action)
        self.image = None
        self.load_image_with_geometry(image_path, geometry)

    def load_image_with_geometry(self, image_path, geometry):
        self.load_image(image_path)
        self.set_image_geometry(geometry)

    def load_image(self, image_path):
        try:
            image = pygame.image.load(image_path)
        except pygame.error as e:
            raise FileNotFoundError(e)
        else:
            image = image.convert()
            image.set_colorkey((255, 255, 255))
            self.image = image

    def set_image_geometry(self, geometry):
        image = pygame.transform.scale(self.image, geometry)
        self.image = image

    def render(self, window, position):
        image_geometry = self.image.get_size()
        final_position = self.get_centre_position_for_widget(position, image_geometry)
        window.blit(self.image, final_position)