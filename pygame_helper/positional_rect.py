import pygame
from pygame.math import Vector2
from multipledispatch import dispatch
from utilities import WHTuple


class PositionalRect(object):

    @dispatch(object, object, object, object)
    def __init__(self, x, y, width, height):
        self._x = float(x)
        self._y = float(y)
        self._width = int(width)
        self._height = int(height)

    @dispatch(object, object)
    def __init__(self, coords, geometry):
        self._x = float(coords[0])
        self._y = float(coords[1])
        self._width = int(geometry[0])
        self._height = int(geometry[1])

    @dispatch(pygame.Rect)
    def __init__(self, rect):
        self._x = float(rect.x)
        self._y = float(rect.y)
        self._width = int(rect.width)
        self._height = int(rect.height)

    
    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = int(value)

    @property
    def w(self):
        return self._width

    @w.setter
    def w(self, value):
        self._width = int(value)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = int(value)

    @property
    def h(self):
        return self._height

    @h.setter
    def h(self, value):
        self._height = int(value)

    @property
    def size(self):
        return WHTuple(self.width, self.height)

    @size.setter
    def size(self, value):
        self.width = value[0]
        self.height = value[1]


    @property
    def x(self):
        return round(self._x)

    @x.setter
    def x(self, value):
        self._x = float(value)

    @property
    def y(self):
        return round(self._y)

    @y.setter
    def y(self, value):
        self._y = float(value)

    
    @property
    def top(self):
        return self.y

    @top.setter
    def top(self, value):
        self.y = value

    @property
    def left(self):
        return self.x

    @left.setter
    def left(self, value):
        self.x = value

    @property
    def bottom(self):
        return self.y + self.height

    @bottom.setter
    def bottom(self, value):
        self.y = value - self.height

    @property
    def right(self):
        return self.x + self.width

    @right.setter
    def right(self, value):
        self.x = value - self.width


    @property
    def centerx(self):
        return round(self._x + (self.width / 2))

    @centerx.setter
    def centerx(self, value):
        self.x = value - (self.width / 2)

    @property
    def centery(self):
        return round(self._y + (self.height / 2))

    @centery.setter
    def centery(self, value):
        self.y = value - (self.height / 2)

    @property
    def center(self):
        return Vector2(self.centerx, self.centery)

    @center.setter
    def center(self, value):
        self.centerx = value[0]
        self.centery = value[1]


    @property
    def topleft(self):
        return Vector2(self.left, self.top)

    @topleft.setter
    def topleft(self, value):
        self.left = value[0]
        self.top = value[1]

    @property
    def bottomleft(self):
        return Vector2(self.left, self.bottom)

    @bottomleft.setter
    def bottomleft(self, value):
        self.left = value[0]
        self.bottom = value[1]

    @property
    def topright(self):
        return Vector2(self.right, self.top)

    @topright.setter
    def topright(self, value):
        self.right = value[0]
        self.top = value[1]

    @property
    def bottomright(self):
        return Vector2(self.right, self.bottom)

    @bottomright.setter
    def bottomright(self, value):
        self.right = value[0]
        self.bottom = value[1]


    @property
    def midtop(self):
        return Vector2(self.centerx, self.top)

    @midtop.setter
    def midtop(self, value):
        self.centerx = value[0]
        self.top = value[1]

    @property
    def midleft(self):
        return Vector2(self.left, self.centery)

    @midleft.setter
    def midleft(self, value):
        self.left = value[0]
        self.centery = value[1]

    @property
    def midbottom(self):
        return Vector2(self.centerx, self.bottom)

    @midbottom.setter
    def midbottom(self, value):
        self.centerx = value[0]
        self.bottom = value[1]

    @property
    def midright(self):
        return Vector2(self.right, self.centery)

    @midright.setter
    def midright(self, value):
        self.right = value[0]
        self.centery = value[1]


    def __repr__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y}, width={self.width}, height={self.height})"

    def __str__(self):
        return f"{self.__class__.__name__}(({self.x}, {self.y}), ({self.width}, {self.height}))"