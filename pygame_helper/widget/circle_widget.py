import pygame
from base_widget import Widget


class CircleWidget(Widget):

    def __init__(self, radius, colour="default", border_thickness=0, action=None):
        super().__init__(action)
        self.radius = 0
        self.colour = None
        self.border_thickness = None

        self.set_radius(radius)
        self.set_colour(colour)
        self.set_border_thickness(border_thickness)

    def set_radius(self, radius):
        self.radius = radius

    def set_colour(self, colour):
        if colour == "default":
            colour = pygame.Color(0, 0, 0)
        self.colour = colour

    def set_border_thickness(self, border_thickness):
        self.border_thickness = border_thickness

    def render(self, window, centre):
        pygame.draw.circle(window, self.colour, centre, self.radius, self.border_thickness)