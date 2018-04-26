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

    @property
    def groPosition(self):
        return self * 150

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
        self._id = -1

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, i):
        self._id = i

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

    @property
    def outer_signal_id(self):
        return 2 * self.id

    @property
    def inner_signal_id(self):
        return self.outer_signal_id + 1

    @property
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

groHeader = """
include gro

set("population_max", 2000);

fun close x y . 
    if x = 0 | y = 0 then
        1.1
    else
        if x > y then
            (x / y - 1) 
        else
            (y / x - 1) 
        end
    end;

MAX_DIFF = 0.5;

"""

groColors = """
    gfp := 0;
    rfp := 0;
    bfp := 0;
    cfp := 0;
    yfp := 0;

"""

class GroPrinter(object):
    def __init__(self):
        self._sstream = ''
        self._indent = 0
        self._signals = 0

    def genPrologue(self):
        self.sstream += groHeader
        return self

    @property
    def sstream(self):
        return self._sstream

    @property
    def indent(self):
        return self._indent

    @property
    def signals(self):
        return self._signals

    @sstream.setter
    def sstream(self, new_sstream):
        self._sstream = new_sstream

    @indent.setter
    def indent(self, new_indent):
        self._indent = new_indent

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.sstream

    @property
    def line_begin(self):
        r = ""
        for i in range(self.indent):
            r += "    "
        return r

    @property
    def line_end(self):
        return "\n"

    @property
    def new_line(self):
        return self.line_end

    def blank_line(self):
        self.sstream += self.new_line
        return self

    def start_program(self, prog):
        self.sstream += self.line_begin + "program {0}() := {{".format(prog) + self.line_end
        self.indent += 1
        return self

    def launch_program(self, prog):
        self.sstream += self.line_begin + "ecoli ( [], program {0}() );".format(prog) + self.line_end
        return self

    def declare_colors(self):
        self.sstream += groColors
        return self

    def color2fluorescent(self, c):
        c = c.lower()
        if c == "red":
            return "rfp"
        elif c == "blue":
            return "bfp"
        elif c == "yellow":
            return "yfp"
        elif c == "cyan":
            return "cfp"
        else:
            return "gfp"

    def set_color(self, c):
        self.sstream += self.line_begin + "{0} := 800;".format(self.color2fluorescent(c)) + self.line_end
        return self

    def unset_color(self, c):
        self.sstream += self.line_begin + "{0} := 0;".format(self.color2fluorescent(c)) + self.line_end
        return self

    def die(self):
        self.sstream += self.line_begin + "die();" + self.line_end
        return self

    def declare_timer(self):
        self.sstream += self.line_begin + "p := [ t := 0 ];" + self.line_end
        self.sstream += self.new_line
        self.sstream += self.line_begin + "true : { p.t := p.t + dt }" + self.line_end
        self.sstream += self.new_line
        return self

    def end_program(self):
        self.indent -= 1
        self.sstream += self.line_begin + "};" + self.line_end
        return self

    @property
    def predicate_always(self):
        return "true"

    def start_command(self, pred):
        self.sstream += self.line_begin + pred + " := {" + self.line_end
        self.indent += 1
        return self

    def end_command(self):
        self.indent -= 1
        self.sstream += self.line_begin + "}" + self.line_end
        return self

    def signal_name(self, s):
        return "signal" + str(s)

    def line_predicates(self, line):
        p1 = "get_signal({0}) >= {2} & get_signal({1}) >= {2} & close (get_signal({0})) (get_signal({1})) <= MAX_DIFF".format(self.signal_name(line.outer_signal_id), self.signal_name(line.inner_signal_id), line.signalStrength)
        p2 = "get_signal({0}) < {2} | get_signal({1}) < {2} | close (get_signal({0})) (get_signal({1})) > MAX_DIFF".format(self.signal_name(line.outer_signal_id), self.signal_name(line.inner_signal_id), line.signalStrength)
        return [p1, p2]

    def intersect(self, preds):
        if len(preds) == 0:
            return "true"
        elif len(preds) == 1:
            return preds[0]
        return "( " + " ) & ( ".join(preds) + " )"

    def union(self, preds):
        if len(preds) == 0:
            return "true"
        elif len(preds) == 1:
            return preds[0]
        return "( " + " ) | ( ".join(preds) + " )"

    def declare_signal(self, sid):
        self.sstream += self.line_begin + "{0} := signal(5, 0.1);".format(self.signal_name(sid)) + self.line_end
        return self

    def init_signal(self, sid, s):
        self.sstream += self.line_begin + "set_signal({0}, {1}, {2}, 100);".format(self.signal_name(sid), s.groPosition.x, s.groPosition.y) + self.line_end
        return self

    def declare_signals_for_lines(self, lines):
        for l in lines:
            self.declare_signal(l.outer_signal_id)
            self.declare_signal(l.inner_signal_id)
        self.blank_line()
        return self

    def init_signals_for_lines(self, lines):
        self.start_program("main")
        self.start_command(self.predicate_always)
        for l in lines:
            signals = l.signals()
            self.init_signal(l.outer_signal_id, signals[0])
            self.init_signal(l.inner_signal_id, signals[1])
        self.end_command()
        self.end_program()
        self.blank_line()
        return self

class Canvas(object):
    def __init__(self, name="canvas"):
        self._lines = []
        self._program = GroPrinter()
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def lines(self):
        return self._lines

    @property
    def program(self):
        return self._program

    @property
    def num_lines(self):
        return len(self.lines)

    def drawLine(self, v0, v1, color='green'):
        l = Line(v0, v1, color)
        l.id = self.num_lines
        self.lines.append(l)
        return self

    def codegen(self):
        p = self.program
        p.genPrologue().declare_signals_for_lines(self.lines)
        p.start_program(self.name).declare_colors().declare_timer()
        unset_color_map = {}
        for l in self.lines:
            preds = p.line_predicates(l)
            c = l.color
            p.start_command(preds[0]).set_color(c).end_command().blank_line()
            if c not in unset_color_map:
                unset_color_map[c] = []
            unset_color_map[c].append(preds[1])
        for c in unset_color_map:
            pred = p.intersect(unset_color_map[c])
            p.start_command(pred).unset_color(c).end_command().blank_line()
        p.end_program().blank_line()
        p.init_signals_for_lines(self.lines)
        p.launch_program(self.name)
        return p
