import math
from typing import Literal, NamedTuple
from dataclasses import dataclass


class Coord(NamedTuple):
    x: int
    y: int


@dataclass
class Action:
    shape: str
    rotate: Literal[-1, 0, 1, 2] = 0
    flip: bool = False
    coord: Coord = Coord(0, 0)


def rotateX(pt, refpt, deg):
    return (refpt[0] + (math.cos(math.radians(deg)) * (pt[0] - refpt[0])) + (math.sin(math.radians(deg)) * (pt[1] - refpt[1])))


def rotateY(pt, refpt, deg):
    return (refpt[1] + (-math.sin(math.radians(deg))*(pt[0] - refpt[0])) + (math.cos(math.radians(deg)) * (pt[1] - refpt[1])))


def rotateP(pt: Coord, refpt: Coord, deg):
    """
    pt: arbitrary point
    refpt: rotation center
    """
    return (int(round(rotateX(pt, refpt, deg))), int(round(rotateY(pt, refpt, deg))))

# SHAPES_DATA = {
#     'I1': {
#         'size': 1,
#         'points': set((Coord(0, 0),)),
#         'corners': set((Coord(1, 1), Coord(-1, -1), Coord(1, -1), Coord(-1, 1)))
#     },
#     'I2': {
#         'size': 2,
#         'points': set((Coord(0, 0), Coord(0, 1))),
#         'corners': set((Coord(1, 2), Coord(-1, -1), Coord(1, -1), Coord(-1, 2)))
#     },

# }


class Shape:
    def __init__(self):
        self.refpt = Coord(0, 0)

    def set_points(self, x, y):
        """
        Set points according to Shape.id
        """
        self.points = []
        self.corners = []

    def place(self, pt: Coord, refpt: Coord):
        """
        Set coords when placed on Board.
        pt: Which point in the shape
        refpt: Which point of the board
        """
        if pt not in self.points:
            raise Exception(f"{pt} not in this shape")
        self.refpt = refpt
        x = refpt[0] - pt[0]
        y = refpt[1] - pt[1]
        self.set_points(x, y)

    def rotate(self, r: int):
        if r == 0:
            return
        deg = r * 90
        self.points = [rotateP(pt, self.refpt, deg) for pt in self.points]
        self.corners = [rotateP(pt, self.refpt, deg) for pt in self.corners]

    def flip(self):
        """
        flip the piece horizontally
        """
        def fliph(pt):
            x1 = self.refpt[0]
            x2 = pt[0]
            x1 = (x1 - (x2 - x1))
            return (x1, pt[1])

        self.points = [fliph(pt) for pt in self.points]
        self.corners = [fliph(pt) for pt in self.corners]



class I1(Shape):
    """
    X
    """
    def __init__(self, x, y):
        self.id = 'I1'
        self.size = 1
        self.set_points(x, y)
        super().__init__()

    def set_points(self, x, y):
        self.points = [(x, y)]
        self.corners = [(x + 1, y + 1), (x - 1, y - 1),
                        (x + 1, y - 1), (x - 1, y + 1)]


class I2(Shape):
    """
    X
    X
    """
    def __init__(self, x, y):
        self.id = 'I2'
        self.size = 2
        self.set_points(x, y)
        super().__init__()

    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1)]
        self.corners = [(x - 1, y - 1), (x + 1, y - 1),
                        (x + 1, y + 2), (x - 1, y + 2)]


class I3(Shape):
    """
    
    """
    def __init__(self, x, y):
        self.id = 'I3'
        self.size = 3
        self.set_points(x, y)
        super().__init__()

    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x, y + 2)]
        self.corners = [(x - 1, y - 1), (x + 1, y - 1),
                        (x + 1, y + 3), (x - 1, y + 3)]


class I4(Shape):
    def __init__(self, x, y):
        self.id = 'I4'
        self.size = 4
        self.set_points(x, y)
        super().__init__()

    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x, y + 2), (x, y + 3)]
        self.corners = [(x - 1, y - 1), (x + 1, y - 1),
                        (x + 1, y + 4), (x - 1, y + 4)]


class I5(Shape):
    def __init__(self, x, y):
        self.id = 'I5'
        self.size = 5
        self.set_points(x, y)
        super().__init__()

    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x, y + 2), (x, y + 3), (x, y + 4)]
        self.corners = [(x - 1, y - 1), (x + 1, y - 1),
                        (x + 1, y + 5), (x - 1, y + 5)]


class V3(Shape):
    def __init__(self, x, y):
        self.id = 'V3'
        self.size = 3
        self.set_points(x, y)
        super().__init__()

    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y)]
        self.corners = [(x - 1, y - 1), (x + 2, y - 1),
                        (x + 2, y + 1), (x + 1, y + 2), (x - 1, y + 2)]


class L4(Shape):
    def __init__(self, x, y):
        self.id = 'L4'
        self.size = 4
        self.set_points(x, y)
        super().__init__()

    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x, y + 2), (x + 1, y)]
        self.corners = [(x - 1, y - 1), (x + 2, y - 1),
                        (x + 2, y + 1), (x + 1, y + 3), (x - 1, y + 3)]


class Z4(Shape):
    def __init__(self, x, y):
        self.id = 'Z4'
        self.size = 4
        self.set_points(x, y)
        super().__init__()

    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y + 1), (x - 1, y)]
        self.corners = [(x - 2, y - 1), (x + 1, y - 1), (x + 2, y),
                        (x + 2, y + 2), (x - 1, y + 2), (x - 2, y + 1)]


class O4(Shape):
    def __init__(self, x, y):
        self.id = 'O4'
        self.size = 4
        self.set_points(x, y)
        super().__init__()

    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y + 1), (x + 1, y)]
        self.corners = [(x - 1, y - 1), (x + 2, y - 1),
                        (x + 2, y + 2), (x - 1, y + 2)]


class L5(Shape):
    def __init__(self, x, y):
        self.id = 'L5'
        self.size = 5
        self.set_points(x, y)
        super().__init__()

    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y), (x + 2, y), (x + 3, y)]
        self.corners = [(x - 1, y - 1), (x + 4, y - 1),
                        (x + 4, y + 1), (x + 1, y + 2), (x - 1, y + 2)]


class T5(Shape):
    def __init__(self, x, y):
        self.id = 'T5'
        self.size = 5
        self.set_points(x, y)
        super().__init__()

    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x, y + 2), (x - 1, y), (x + 1, y)]
        self.corners = [(x + 2, y - 1), (x + 2, y + 1), (x + 1, y + 3),
                        (x - 1, y + 3), (x - 2, y + 1), (x - 2, y - 1)]


class V5(Shape):
    def __init__(self, x, y):
        self.id = 'V5'
        self.size = 5
        self.set_points(x, y)
        super().__init__()

    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x, y + 2), (x + 1, y), (x + 2, y)]
        self.corners = [(x - 1, y - 1), (x + 3, y - 1),
                        (x + 3, y + 1), (x + 1, y + 3), (x - 1, y + 3)]


class N(Shape):
    def __init__(self, x, y):
        self.id = 'N'
        self.size = 5
        self.set_points(x, y)
        super().__init__()

    def set_points(self, x, y):
        self.points = [(x, y), (x + 1, y), (x + 2, y),
                       (x, y - 1), (x - 1, y - 1)]
        self.corners = [(x + 1, y - 2), (x + 3, y - 1), (x + 3,
                                                         y + 1), (x - 1, y + 1), (x - 2, y), (x - 2, y - 2)]


class Z5(Shape):
    def __init__(self, x, y):
        self.id = 'Z5'
        self.size = 5
        self.set_points(x, y)
        super().__init__()

    def set_points(self, x, y):
        self.points = [(x, y), (x + 1, y), (x + 1, y + 1),
                       (x - 1, y), (x - 1, y - 1)]
        self.corners = [(x + 2, y - 1), (x + 2, y + 2), (x, y + 2),
                        (x - 2, y + 1), (x - 2, y - 2), (x, y - 2)]


class T4(Shape):
    def __init__(self, x, y):
        self.id = 'T4'
        self.size = 4
        self.set_points(x, y)
        super().__init__()

    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y), (x - 1, y)]
        self.corners = [(x + 2, y - 1), (x + 2, y + 1), (x + 1, y + 2),
                        (x - 1, y + 2), (x - 2, y + 1), (x - 2, y - 1)]


class P(Shape):
    def __init__(self, x, y):
        self.id = 'P'
        self.size = 5
        self.set_points(x, y)
        super().__init__()

    def set_points(self, x, y):
        self.points = [(x, y), (x + 1, y), (x + 1, y - 1),
                       (x, y - 1), (x, y - 2)]
        self.corners = [(x + 1, y - 3), (x + 2, y - 2),
                        (x + 2, y + 1), (x - 1, y + 1), (x - 1, y - 3)]


class W(Shape):
    def __init__(self, x, y):
        self.id = 'W'
        self.size = 5
        self.set_points(x, y)
        super().__init__()

    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y + 1),
                       (x - 1, y), (x - 1, y - 1)]
        self.corners = [(x + 1, y - 1), (x + 2, y), (x + 2, y + 2),
                        (x - 1, y + 2), (x - 2, y + 1), (x - 2, y - 2), (x, y - 2)]


class U(Shape):
    def __init__(self, x, y):
        self.id = 'U'
        self.size = 5
        self.set_points(x, y)
        super().__init__()

    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y + 1),
                       (x, y - 1), (x + 1, y - 1)]
        self.corners = [(x + 2, y - 2), (x + 2, y),
                        (x + 2, y + 2), (x - 1, y + 2), (x - 1, y - 2)]


class F(Shape):
    def __init__(self, x, y):
        self.id = 'F'
        self.size = 5
        self.set_points(x, y)
        super().__init__()

    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y + 1),
                       (x, y - 1), (x - 1, y)]
        self.corners = [(x + 1, y - 2), (x + 2, y), (x + 2, y + 2),
                        (x - 1, y + 2), (x - 2, y + 1), (x - 2, y - 1), (x - 1, y - 2)]


class X(Shape):
    def __init__(self, x, y):
        self.id = 'X'
        self.size = 5
        self.set_points(x, y)
        super().__init__()

    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]
        self.corners = [(x + 1, y - 2), (x + 2, y - 1), (x + 2, y + 1), (x + 1, y + 2),
                        (x - 1, y + 2), (x - 2, y + 1), (x - 2, y - 1), (x - 1, y - 2)]


class Y(Shape):
    def __init__(self, x, y):
        self.id = 'Y'
        self.size = 5
        self.set_points(x, y)
        super().__init__()

    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y), (x + 2, y), (x - 1, y)]
        self.corners = [(x + 3, y - 1), (x + 3, y + 1), (x + 1, y + 2),
                        (x - 1, y + 2), (x - 2, y + 1), (x - 2, y - 1)]


SHAPES_ID = set(('I1', 'I2', 'I3', 'I4', 'I5', 'V3', 'L4', 'Z4', 'O4',
                 'L5', 'T5', 'V5', 'N', 'Z5', 'T4', 'P', 'W', 'U', 'F', 'X', 'Y'))
"""IDs of all the shapes"""

SHAPES_CLASS: dict[str, Shape] = {
    'I1': I1,
    'I2': I2,
    'I3': I3,
    'I4': I4,
    'I5': I5,
    'V3': V3,
    'L4': L4,
    'Z4': Z4,
    'O4': O4,
    'L5': L5,
    'T5': T5,
    'V5': V5,
    'N': N,
    'Z5': Z5,
    'T4': T4,
    'P': P,
    'W': W,
    'U': U,
    'F': F,
    'X': X,
    'Y': Y
}
"""Maps id to Shape classes"""
