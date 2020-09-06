import pygame
from pygame.math import Vector2
from multipledispatch import dispatch


class VectorRect(Vector2):

    @dispatch()
    def __init__(self):
        super().__init__()
        self.width = float(0)
        self.height = float(0)

    @dispatch(Vector2, object, object)
    def __init__(self, vector, width, height):
        super().__init__(vector)
        self.width = float(width)
        self.height = float(height)

    @dispatch(Vector2, object)
    def __init__(self, vector, geometry):
        super().__init__(vector)
        self.width = float(geometry[0])
        self.height = float(geometry[1])

    @dispatch(object, object, object, object)
    def __init__(self, x, y, width, height):
        super().__init__(x, y)
        self.width = float(width)
        self.height = float(height)

    @dispatch(object, object)
    def __init__(self, coords, geometry):
        super().__init__(coords)
        self.width = float(geometry[0])
        self.height = float(geometry[1])
