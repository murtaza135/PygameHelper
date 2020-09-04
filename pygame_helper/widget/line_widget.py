import pygame
from base_widget import Widget


class LineWidget(Widget):

    def __init__(self, line_vector, colour="default", thickness=0, action=None):
        super().__init__(action)
        self.line_vector = None
        self.colour = None
        self.thickness = None

        self.set_line_vector(line_vector)
        self.set_colour(colour)
        self.set_thickness(thickness)

    def set_line_vector(self, line_vector):
        self.line_vector = line_vector

    def set_colour(self, colour):
        if colour == "default":
            colour = pygame.Color(0, 0, 0)
        self.colour = colour

    def set_thickness(self, thickness):
        self.thickness = thickness

    def render(self, window, start_position):
        end_position = (start_position[0] + self.line_vector[0], start_position[1] + self.line_vector[1])
        pygame.draw.line(window, self.colour, start_position, end_position, self.thickness)