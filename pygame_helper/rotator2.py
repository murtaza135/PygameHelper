from pygame.math import Vector2
from multipledispatch import dispatch
import math
import exceptions


class Rotator2(object):

    LEFT = 180
    RIGHT = 0
    UP = 90
    DOWN = -90

    @dispatch()
    def __init__(self):
        self.set_rotator()

    @dispatch(int)
    def __init__(self, number):
        self.set_rotator(number)

    @dispatch(float)
    def __init__(self, number):
        self.set_rotator(number)

    @dispatch(object)
    def __init__(self, rotator):
        self.set_rotator(rotator)

    @dispatch(Vector2)
    def __init__(self, vector):
        self.set_rotator(vector)

    @dispatch()
    def set_rotator(self):
        self.rotator = float(0)

    @dispatch(int)
    def set_rotator(self, number):
        number = self._set_rotator_between_minus_180_and_180(number)
        self.rotator = float(number)

    @dispatch(float)
    def set_rotator(self, number):
        number = self._set_rotator_between_minus_180_and_180(number)
        self.rotator = float(number)

    @dispatch(object)
    def set_rotator(self, rotator):
        if not isinstance(rotator, Rotator2):
            raise TypeError("Must provide a number, Rotator2 or Vector2")

        rotator = self._set_rotator_between_minus_180_and_180(rotator.rotator)
        self.rotator = float(rotator)

    @dispatch(Vector2)
    def set_rotator(self, vector):
        if vector.x == 0 and vector.y == 0:
            raise ValueError("Could not create Rotator - magnitude of vector cannot be 0")

        positive_x_axis_vector = Vector2(1, 0)
        dot_product_value = positive_x_axis_vector.dot(vector)
        cos_of_angle_between_vectors = dot_product_value / (vector.magnitude() * positive_x_axis_vector.magnitude())
        angle_between_vectors_in_radians = math.acos(cos_of_angle_between_vectors)
        angle_between_vectors_in_degrees = math.degrees(angle_between_vectors_in_radians)
        if vector.y < 0:
            angle_between_vectors_in_degrees *= -1
        self.set_rotator(angle_between_vectors_in_degrees)

    def _set_rotator_between_minus_180_and_180(self, rotator_value):
        FULL_CIRCLE_DEGREES = 360
        LOWER_BOUNDARY = -180
        UPPER_BOUNDARY = 180

        rotator_value %= FULL_CIRCLE_DEGREES
        while rotator_value <= LOWER_BOUNDARY:
            rotator_value += FULL_CIRCLE_DEGREES
        while rotator_value > UPPER_BOUNDARY:
            rotator_value -= FULL_CIRCLE_DEGREES

        return rotator_value

    def get_vector(self):
        rotator_in_radians = math.radians(self.rotator)
        return Vector2(
            round(math.cos(rotator_in_radians), 10),
            round(math.sin(rotator_in_radians), 10)
        )

    def __repr__(self):
        return f"Rotator2({self.rotator})"

    def __str__(self):
        return f"{self.rotator}°"

    def __setattr__(self, name, number):
        if not isinstance(number, (int, float)):
            raise TypeError("Must provide a number")

        number = self._set_rotator_between_minus_180_and_180(number)
        super().__setattr__(name, float(number))

    def __delattr__(self, name):
        raise exceptions.DeleteError("Cannot delete attribute")

    def __add__(self, rotator):
        if not isinstance(rotator, Rotator2):
            raise TypeError("Must provide another rotator")

        rotator_value = self.rotator + rotator.rotator
        rotator_value = self._set_rotator_between_minus_180_and_180(rotator_value)
        return Rotator2(rotator_value)

    def __sub__(self, rotator):
        if not isinstance(rotator, Rotator2):
            raise TypeError("Must provide another rotator")

        rotator_value = self.rotator - rotator.rotator
        rotator_value = self._set_rotator_between_minus_180_and_180(rotator_value)
        return Rotator2(rotator_value)

    def __mul__(self, number):
        if not isinstance(number, (int, float)):
            raise TypeError("Must provide a number")

        rotator_value = self.rotator * number
        rotator_value = self._set_rotator_between_minus_180_and_180(rotator_value)
        return Rotator2(rotator_value)

    def __truediv__(self, number):
        if not isinstance(number, (int, float)):
            raise TypeError("Must provide a number")

        rotator_value = self.rotator / number
        rotator_value = self._set_rotator_between_minus_180_and_180(rotator_value)
        return Rotator2(rotator_value)

    def __floordiv__(self, number):
        if not isinstance(number, (int, float)):
            raise TypeError("Must provide a number")

        rotator_value = self.rotator // number
        rotator_value = self._set_rotator_between_minus_180_and_180(rotator_value)
        return Rotator2(rotator_value)

    def __mod__(self, number):
        if not isinstance(number, (int, float)):
            raise TypeError("Must provide a number")

        rotator_value = self.rotator % number
        rotator_value = self._set_rotator_between_minus_180_and_180(rotator_value)
        return Rotator2(rotator_value)

    def __iadd__(self, rotator):
        if not isinstance(rotator, Rotator2):
            raise TypeError("Must provide another rotator")

        rotator_value = self.rotator + rotator.rotator
        self.set_rotator(rotator_value)
        return self

    def __isub__(self, rotator):
        if not isinstance(rotator, Rotator2):
            raise TypeError("Must provide another rotator")

        rotator_value = self.rotator - rotator.rotator
        self.set_rotator(rotator_value)
        return self

    def __imul__(self, number):
        if not isinstance(number, (int, float)):
            raise TypeError("Must provide a number")

        rotator_value = self.rotator * number
        self.set_rotator(rotator_value)
        return self

    def __itruediv__(self, number):
        if not isinstance(number, (int, float)):
            raise TypeError("Must provide a number")

        rotator_value = self.rotator / number
        self.set_rotator(rotator_value)
        return self

    def __ifloordiv__(self, number):
        if not isinstance(number, (int, float)):
            raise TypeError("Must provide a number")

        rotator_value = self.rotator // number
        self.set_rotator(rotator_value)
        return self

    def __imod__(self, number):
        if not isinstance(number, (int, float)):
            raise TypeError("Must provide a number")

        rotator_value = self.rotator % number
        self.set_rotator(rotator_value)
        return self

    def __lt__(self, rotator):
        if not isinstance(rotator, Rotator2):
            raise TypeError("Must provide another rotator")

        return self.rotator < rotator.rotator

    def __le__(self, rotator):
        if not isinstance(rotator, Rotator2):
            raise TypeError("Must provide another rotator")

        return self.rotator <= rotator.rotator

    def __eq__(self, rotator):
        if not isinstance(rotator, Rotator2):
            raise TypeError("Must provide another rotator")

        return self.rotator == rotator.rotator

    def __ne__(self, rotator):
        if not isinstance(rotator, Rotator2):
            raise TypeError("Must provide another rotator")

        return self.rotator != rotator.rotator

    def __gt__(self, rotator):
        if not isinstance(rotator, Rotator2):
            raise TypeError("Must provide another rotator")

        return self.rotator > rotator.rotator

    def __ge__(self, rotator):
        if not isinstance(rotator, Rotator2):
            raise TypeError("Must provide another rotator")

        return self.rotator >= rotator.rotator

    def __neg__(self):
        rotator_value = self._set_rotator_between_minus_180_and_180(-self.rotator)
        return Rotator2(rotator_value)

    def __abs__(self):
        rotator_value = self._set_rotator_between_minus_180_and_180(abs(self.rotator))
        return Rotator2(rotator_value)