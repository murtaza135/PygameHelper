import pygame
from dotmap import DotMap
import pygame_helper.exceptions as exceptions


class WidgetLayout(pygame.Surface):
    
    def __init__(self, geometry, flags=0):
        if not pygame.display.get_init():
            raise exceptions.PygameInitError
        
        super().__init__(geometry, flags)
        self.fill((0, 0, 0, 255))
        self.widgets = DotMap()
        self.widgets_ordered = list()

    def add_widget(self, widget, screen_position, render_position="end", name=None):
        if render_position == "end":
            render_position = len(self.widgets_ordered)
        if name is not None and not isinstance(name, basestring):
            raise TypeError("Name must be a string object")

        widget_name = self._generate_widget_name(widget) if name==None else name
        self.widgets[widget_name] = DotMap(widget=widget, screen_position=screen_position)
        self.widgets_ordered.insert(render_position, widget_name)

    def _generate_widget_name(self, widget):
        class_name_of_widget = type(widget).__name__
        number_suffix = 0
        for name in self.widgets.keys():
            if class_name_of_widget in name:
                number_suffix += 1
        widget_name = f"{class_name_of_widget}_{number_suffix}"
        return widget_name

    def change_widget_name(self, old_widget_name, new_widget_name):
        if not isinstance(new_widget_name, basestring):
            raise TypeError("New widget name must be a string object")

        widget_info =  self.widgets[old_widget_name]
        del self.widgets[old_widget_name]
        self.widgets[new_widget_name] = widget_info

        widget_render_position = self.widgets_ordered.index(old_widget_name)
        self.widgets_ordered[widget_render_position] = new_widget_name

    def change_widget_screen_position(self, widget_name, new_screen_position):
        self.widgets[widget_name]["screen_position"] = new_screen_position

    def change_widget_render_position(self, widget_name, render_position):
        self.widgets_ordered.remove(widget_name)
        self.widgets_ordered.insert(render_position, widget_name)

    def delete_widget(self, widget_name):
        del self.widgets[widget_name]
        self.widgets_ordered.remove(widget_name)

    def print_order_of_widgets(self):
        for num, widget_name in enumerate(self.widgets_ordered):
            print(f"{num}) {widget_name}")

    def print_widget_details(self, widget_name):
        print(self.widgets[widget_name])

    def render(self, window, position=(0, 0), size="entire_window"):
        self._render_widgets_on_widget_layout()
        self._render_widget_layout_on_window(window, position, size)

    def _render_widgets_on_widget_layout(self):
        for widget_name in self.widgets_ordered:
            self.widgets[widget_name]["widget"].render(
                window=self,
                position=self.widgets[widget_name]["screen_position"]
            )

    def _render_widget_layout_on_window(self, window, position=(0, 0), size="entire_window"):
        if size == "entire_window":
            size = window.get_size()
        elif size == "original":
            size = self.get_size()
        menu = pygame.transform.scale(self, size)
        window.blit(menu, position)