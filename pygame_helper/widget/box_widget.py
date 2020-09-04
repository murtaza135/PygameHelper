import pygame
from base_widget import Widget


class BoxWidget(Widget):

    def __init__(self, dimensions, colour="default", border_thickness=0, action=None):
        super().__init__(action)
        self.dimensions = None
        self.colour = None
        self.border_thickness = None
        self.rounded_corners = None

        self.set_dimensions(dimensions)
        self.set_colour(colour)
        self.set_border_thickness(border_thickness)
        self.set_rounded_corners()

    def set_dimensions(self, dimensions):
        self.dimensions = dimensions

    def set_colour(self, colour):
        if colour == "default":
            colour = pygame.Color(0, 0, 0)
        self.colour = colour

    def set_border_thickness(self, border_thickness):
        self.border_thickness = border_thickness

    def set_rounded_corners(self, all_corners=0, top_left=0, top_right=0, bottom_left=0, bottom_right=0):
        self.rounded_corners = {
            "border_radius": all_corners,
            "border_top_left_radius": top_left,
            "border_top_right_radius": top_right,
            "border_bottom_left_radius": bottom_left,
            "border_bottom_right_radius": bottom_right
        }

    def render(self, window, position):
        final_position = self.get_centre_position_for_widget(position, self.dimensions)
        pygame.draw.rect(
            window,
            self.colour,
            final_position + self.dimensions,
            self.border_thickness
        )