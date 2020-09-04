import pygame
from base_widget import Widget


class TextWidget(Widget):

    def __init__(self, text, colour="default", font="default", action=None):
        super().__init__(action)
        self.text = None
        self.colour = None
        self.font = None

        self.set_text(text)
        self.set_colour(colour)
        self.set_font(font)

    def set_text(self, text):
        self.text = text

    def set_colour(self, colour):
        if colour == "default":
            colour = pygame.Color(0, 0, 0)
        self.colour = colour

    def set_font(self, font):
        if font == "default":
            font = pygame.font.SysFont("calibri", 35, True)
        self.font = font

    def render_new_text(self, text, window, position):
        self.set_text(text)
        self.render(window, position)

    def render(self, window, position):
        text_to_be_rendered = self.font.render(self.text, True, self.colour)
        text_size = text_to_be_rendered.get_size()
        final_position = self.get_centre_position_for_widget(position, text_size)
        window.blit(text_to_be_rendered, final_position)