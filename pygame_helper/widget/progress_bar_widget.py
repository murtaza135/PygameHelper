import pygame
from base_widget import Widget


class ProgressBarWidget(Widget):

    def __init__(self, dimensions, bg_colour="default", fg_colour="default", progress_value=0, text_widget=None, action=None):
        super().__init__(action)
        self.dimensions = None
        self.background_bar_colour = None
        self.foreground_bar_colour = None
        self.progress_value = 0
        self.text_widget = None

        self.set_dimensions(dimensions)
        self.set_colours(bg_colour, fg_colour)
        self.set_progress_value(progress_value)
        self.set_text_widget(text_widget)

    def set_dimensions(self, dimensions):
        self.dimensions = dimensions

    def set_colours(self, bg_colour, fg_colour):
        if bg_colour == "default":
            bg_colour = pygame.Color(255, 0, 0)
        if fg_colour == "default":
            fg_colour = pygame.Color(0, 255, 0)

        self.background_bar_colour = bg_colour
        self.foreground_bar_colour = fg_colour

    def set_progress_value(self, progress_value):
        if not 0 <= progress_value <= 1:
            raise ValueError("Progress value must lie between 0 and 1")
        self.progress_value = float(progress_value)

    def set_text_widget(self, text_widget):
        self.text_widget = text_widget

    def set_progress_value_then_render(self, progress_value, window, position):
        self.set_progress_value(progress_value)
        self.render(window, position)

    def render(self, window, position):
        self._render_progress_bar(window, position)
        self._render_progress_bar_text(window, position)

    def _render_progress_bar(self, window, position):
        final_position = self.get_centre_position_for_widget(position, self.dimensions)
        pygame.draw.rect(window, self.background_bar_colour, final_position + self.dimensions)
        foreground_bar_new_dimensions = (self.dimensions[0] * self.progress_value, self.dimensions[1])
        pygame.draw.rect(window, self.foreground_bar_colour, final_position + foreground_bar_new_dimensions)

    def _render_progress_bar_text(self, window, centre_position_on_progress_bar):
        if self.text_widget is not None:
            self.text_widget.render(window, centre_position_on_progress_bar)