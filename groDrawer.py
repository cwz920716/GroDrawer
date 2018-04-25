import sys
import math
import random
import numpy as np

class Vec2(object):
    def __init__(self, x, y):
        self._x = float(x)
        self._y = float(y)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new_x):
        self._x = float(new_x)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, new_y):
        self._y = float(new_y)

    def __add__(self, other):
        types = (int, float)
        if isinstance(self, types):
            return Vec2(self + other.x, self + other.y)
        elif isinstance(other, types):
            return Vec2(self.x + other, self.y + other)
        else:
            return Vec2(self.x + other.x, self.y + other.y)

    def __truediv__(self, other):
        types = (int, float)
        if isinstance(self, types):
            self = Vec2(self, self)
        elif isinstance(other, types):
            other = Vec2(other, other)
        x = self.x / other.x
        y = self.y / other.y
        return Vec2(x, y)

    def __mul__(self, other):
        types = (int, float)
        if isinstance(self, types):
            return Vec2(self * other.x, self * other.y)
        elif isinstance(other, types):
            return Vec2(self.x * other, self.y * other)
        else:
            return Vec2(self.x * other.x, self.y * other.y)

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __radd__(self, other):
        return Vec2(self.x + other, self.y + other)

    def __rdiv__(self, other):
        return Vec2(other/self.x, other/self.y)

    def __rmul__(self, other):
        return Vec2(other * self.x, other * self.y)

    def __rsub__(self, other):
        return Vec2(other - self.x, other - self.y)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "[{0}, {1}]".format(self.x, self.y)

    def __sub__(self, other):
        types = (int, float)
        if isinstance(self, types):
            return Vec2(self - other.x, self - other.y)
        elif isinstance(other, types):
            return Vec2(self.x - other, self.y - other)
        else:
            return Vec2(self.x - other.x, self.y - other.y)

    def ceil(self):
        return Vec2(math.ceil(self.x), math.ceil(self.y))

    def floor(self):
        return Vec2(math.floor(self.x), math.floor(self.y))

    def get_data(self):
        return (self.x, self.y)    

    def inverse(self):
        return Vec2(1.0/self.x, 1.0/self.y)

    def length(self):
        return math.sqrt(self.square_length())

    def normalize(self):
        length = self.length()
        if length == 0.0:
            return Vec2(0, 0)
        return Vec2(self.x/length, self.y/length)

    def round(self):
        return Vec2(round(self.x), round(self.y))

    def square_length(self):
        return (self.x * self.x) + (self.y * self.y)

    def rotate90(self):
        return Vec2(-self.y, self.x)

    @classmethod
    def distance(cls, a, b):
        c = b - a
        return c.length()

    @classmethod
    def dot(self, a, b):
        return (a.x * b.x) + (a.y * b.y)

    @classmethod
    def equals(cls, a, b, tolerance=0.0):
        diff = a - b
        dx = math.fabs(diff.x)
        dy = math.fabs(diff.y)
        if dx <= tolerance * max(1, math.fabs(a.x), math.fabs(b.x)) and \
           dy <= tolerance * max(1, math.fabs(a.y), math.fabs(b.y)):
            return True
        return False

    @classmethod
    def max(cls, a, b):
        x = max(a.x, b.x)
        y = max(a.y, b.y)
        return Vec2(x, y)

    @classmethod
    def min(cls, a, b):
        x = min(a.x, b.x)
        y = min(a.y, b.y)
        return Vec2(x, y)

    @classmethod
    def mix(cls, a, b, t):
        return a * t + b * (1-t)

    @classmethod
    def random(cls):
        x = random.random()
        y = random.random()
        return Vec2(x, y)

    @classmethod
    def square_distance(cls, a, b):
        c = b - a
        return c.square_length()

class Point(Vec2):
    pass

"""
    Linear intERPolate between a and b for x ranging from 0 to 1
"""
def lerp(a, b, x):
    return a * (1.0 - x) + b * x

class Line(object):
    def __init__ (self, v0, v1, color = 'green'):
        self._v0 = v0
        self._v1 = v1
        if self.length < 0.5:
            print("WARNING: line length < 0.5 is hard to visualize using gro.")
        if self.length > 5.0:
            print("WARNING: line length > 5.0 is too large for gro screen.")
        self._color = color

    @property
    def v0(self):
        return self._v0

    @v0.setter
    def v0(self, v):
        self._v0 = v

    @property
    def v1(self):
        return self._v1

    @v1.setter
    def v1(self, v):
        self._v1 = v

    @property
    def color(self):
        return self._color

    @property
    def vector(self):
        return self.v1 - self.v0

    @property
    def dir(self):
        return self.vector.normalize()

    @property
    def length(self):
        return self.vector.length()

    @property
    def center(self):
        return (self.v1 + self.v0) / 2.0

    def signals(self):
        d = self.dir.rotate90()
        outer_s = self.center + d
        inner_s = self.center - d
        return [outer_s, inner_s]

    def signalStrength(self):
        l = self.length
        if l <= 0.5:
            return 0.7
        elif l > 0.5 and l <= 1.0:
            x = (l - 0.5) / (1.0 - 0.5)
            return lerp(0.7, 0.5, x)
        elif l > 1.0 and l <= 1.5:
            x = (l - 1.0) / (1.5 - 1.0)
            return lerp(0.5, 0.375, x)
        elif l > 1.5 and l <= 2.0:
            x = (l - 1.5) / (2.0 - 1.5)
            return lerp(0.375, 0.25, x)
        elif l > 2.0 and l <= 2.5:
            x = (l - 2.0) / (2.5 - 2.0)
            return lerp(0.25, 0.175, x)
        elif l > 2.5 and l <= 3.0:
            x = (l - 2.5) / (3.0 - 2.5)
            return lerp(0.175, 0.1, x)
        elif l > 3.0 and l <= 4.0:
            x = (l - 3.0) / (4.0 - 3.0)
            return lerp(0.1, 0.01, x)
        elif l > 4.0 and l <= 5.0:
            x = (l - 4.0) / (5.0 - 4.0)
            return lerp(0.01, 0.005, x)
        else:
            return 0.005

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "{0} -> {1} color={2}".format(self.v0, self.v1, self.color)

class Canvas(object):
    def __init__(self):
        self._lines = []

    @property
    def lines(self):
        return self._lines

    def drawLine(self, v0, v1, color='green'):
        self.lines.append(Line(v0, v1, color))
        return self

x = Point(0, 1.25)
y = Point(0, -0.5)
l = Line(y, x)
x = x / 2
print(l)
print(l.signals())
print(l.signalStrength())
