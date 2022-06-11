import math


def rotateX(pt, refpt, deg):
    return (refpt[0] + (math.cos(math.radians(deg)) * (pt[0] - refpt[0])) + (math.sin(math.radians(deg)) * (pt[1] - refpt[1])))


def rotateY(pt, refpt, deg):
    return (refpt[1] + (-math.sin(math.radians(deg))*(pt[0] - refpt[0])) + (math.cos(math.radians(deg)) * (pt[1] - refpt[1])))


def rotateP(pt, refpt, deg):
    return (int(round(rotateX(pt, refpt, deg))), int(round(rotateY(pt, refpt, deg))))

class Shape:
    def __init__(self, id, size, x, y):
        self.id = id
        self.size = size
        

    def setpoints(self, x, y):
        self.points = []
        self.corners = []

    def create(self, num, pt):
        self.setpoints(0, 0)
        pm = self.points
        self.ptsmap = pm
        self.refpt = pt
        x = pt[0] - self.ptsmap[num][0]
        y = pt[1] - self.ptsmap[num][1]
        self.setpoints(x, y)

    def rotate(self, deg):
        self.points = [rotateP(pt, self.refpt, deg) for pt in self.points]
        self.corners = [rotateP(pt, self.refpt, deg) for pt in self.corners]

    def flip(self, orientation):
        def fliph(pt):
            x1 = self.refpt[0]
            x2 = pt[0]
            x1 = (x1 - (x2 - x1))
            return (x1, pt[1])  # flip the piece horizontally
        if orientation == 'h':
            self.points = [fliph(pt) for pt in self.points]
            self.corners = [fliph(pt) for pt in self.corners]


class I1(Shape):
    def __init__(self):
        self.id = 'I1'
        self.size = 1

    def setpoints(self, x, y):
        self.points = [(x, y)]
        self.corners = [(x + 1, y + 1), (x - 1, y - 1),
                        (x + 1, y - 1), (x - 1, y + 1)]


class I2(Shape):
    def __init__(self):
        self.id = 'I2'
        self.size = 2

    def setpoints(self, x, y):
        self.points = [(x, y), (x, y + 1)]
        self.corners = [(x - 1, y - 1), (x + 1, y - 1),
                        (x + 1, y + 2), (x - 1, y + 2)]


class I3(Shape):
    def __init__(self):
        self.id = 'I3'
        self.size = 3

    def setpoints(self, x, y):
        self.points = [(x, y), (x, y + 1), (x, y + 2)]
        self.corners = [(x - 1, y - 1), (x + 1, y - 1),
                        (x + 1, y + 3), (x - 1, y + 3)]


class I4(Shape):
    def __init__(self):
        self.id = 'I4'
        self.size = 4

    def setpoints(self, x, y):
        self.points = [(x, y), (x, y + 1), (x, y + 2), (x, y + 3)]
        self.corners = [(x - 1, y - 1), (x + 1, y - 1),
                        (x + 1, y + 4), (x - 1, y + 4)]


class I5(Shape):
    def __init__(self):
        self.id = 'I5'
        self.size = 5

    def setpoints(self, x, y):
        self.points = [(x, y), (x, y + 1), (x, y + 2), (x, y + 3), (x, y + 4)]
        self.corners = [(x - 1, y - 1), (x + 1, y - 1),
                        (x + 1, y + 5), (x - 1, y + 5)]


class V3(Shape):
    def __init__(self):
        self.id = 'V3'
        self.size = 3

    def setpoints(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y)]
        self.corners = [(x - 1, y - 1), (x + 2, y - 1),
                        (x + 2, y + 1), (x + 1, y + 2), (x - 1, y + 2)]


class L4(Shape):
    def __init__(self):
        self.id = 'L4'
        self.size = 4

    def setpoints(self, x, y):
        self.points = [(x, y), (x, y + 1), (x, y + 2), (x + 1, y)]
        self.corners = [(x - 1, y - 1), (x + 2, y - 1),
                        (x + 2, y + 1), (x + 1, y + 3), (x - 1, y + 3)]


class Z4(Shape):
    def __init__(self):
        self.id = 'Z4'
        self.size = 4

    def setpoints(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y + 1), (x - 1, y)]
        self.corners = [(x - 2, y - 1), (x + 1, y - 1), (x + 2, y),
                        (x + 2, y + 2), (x - 1, y + 2), (x - 2, y + 1)]


class O4(Shape):
    def __init__(self):
        self.id = 'O4'
        self.size = 4

    def setpoints(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y + 1), (x + 1, y)]
        self.corners = [(x - 1, y - 1), (x + 2, y - 1),
                        (x + 2, y + 2), (x - 1, y + 2)]


class L5(Shape):
    def __init__(self):
        self.id = 'L5'
        self.size = 5

    def setpoints(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y), (x + 2, y), (x + 3, y)]
        self.corners = [(x - 1, y - 1), (x + 4, y - 1),
                        (x + 4, y + 1), (x + 1, y + 2), (x - 1, y + 2)]


class T5(Shape):
    def __init__(self):
        self.id = 'T5'
        self.size = 5

    def setpoints(self, x, y):
        self.points = [(x, y), (x, y + 1), (x, y + 2), (x - 1, y), (x + 1, y)]
        self.corners = [(x + 2, y - 1), (x + 2, y + 1), (x + 1, y + 3),
                        (x - 1, y + 3), (x - 2, y + 1), (x - 2, y - 1)]


class V5(Shape):
    def __init__(self):
        self.id = 'V5'
        self.size = 5

    def setpoints(self, x, y):
        self.points = [(x, y), (x, y + 1), (x, y + 2), (x + 1, y), (x + 2, y)]
        self.corners = [(x - 1, y - 1), (x + 3, y - 1),
                        (x + 3, y + 1), (x + 1, y + 3), (x - 1, y + 3)]


class N(Shape):
    def __init__(self):
        self.id = 'N'
        self.size = 5

    def setpoints(self, x, y):
        self.points = [(x, y), (x + 1, y), (x + 2, y),
                       (x, y - 1), (x - 1, y - 1)]
        self.corners = [(x + 1, y - 2), (x + 3, y - 1), (x + 3,
                                                         y + 1), (x - 1, y + 1), (x - 2, y), (x - 2, y - 2)]


class Z5(Shape):
    def __init__(self):
        self.id = 'Z5'
        self.size = 5

    def setpoints(self, x, y):
        self.points = [(x, y), (x + 1, y), (x + 1, y + 1),
                       (x - 1, y), (x - 1, y - 1)]
        self.corners = [(x + 2, y - 1), (x + 2, y + 2), (x, y + 2),
                        (x - 2, y + 1), (x - 2, y - 2), (x, y - 2)]


class T4(Shape):
    def __init__(self):
        self.id = 'T4'
        self.size = 4

    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y), (x - 1, y)]
        self.corners = [(x + 2, y - 1), (x + 2, y + 1), (x + 1, y + 2),
                        (x - 1, y + 2), (x - 2, y + 1), (x - 2, y - 1)]


class P(Shape):
    def __init__(self):
        self.id = 'P'
        self.size = 5

    def setpoints(self, x, y):
        self.points = [(x, y), (x + 1, y), (x + 1, y - 1),
                       (x, y - 1), (x, y - 2)]
        self.corners = [(x + 1, y - 3), (x + 2, y - 2),
                        (x + 2, y + 1), (x - 1, y + 1), (x - 1, y - 3)]


class W(Shape):
    def __init__(self):
        self.id = 'W'
        self.size = 5

    def setpoints(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y + 1),
                       (x - 1, y), (x - 1, y - 1)]
        self.corners = [(x + 1, y - 1), (x + 2, y), (x + 2, y + 2),
                        (x - 1, y + 2), (x - 2, y + 1), (x - 2, y - 2), (x, y - 2)]


class U(Shape):
    def __init__(self):
        self.id = 'U'
        self.size = 5

    def setpoints(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y + 1),
                       (x, y - 1), (x + 1, y - 1)]
        self.corners = [(x + 2, y - 2), (x + 2, y),
                        (x + 2, y + 2), (x - 1, y + 2), (x - 1, y - 2)]


class F(Shape):
    def __init__(self):
        self.id = 'F'
        self.size = 5

    def setpoints(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y + 1),
                       (x, y - 1), (x - 1, y)]
        self.corners = [(x + 1, y - 2), (x + 2, y), (x + 2, y + 2),
                        (x - 1, y + 2), (x - 2, y + 1), (x - 2, y - 1), (x - 1, y - 2)]


class X(Shape):
    def __init__(self):
        self.id = 'X'
        self.size = 5

    def setpoints(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]
        self.corners = [(x + 1, y - 2), (x + 2, y - 1), (x + 2, y + 1), (x + 1, y + 2),
                        (x - 1, y + 2), (x - 2, y + 1), (x - 2, y - 1), (x - 1, y - 2)]


class Y(Shape):
    def __init__(self):
        self.id = 'Y'
        self.size = 5

    def setpoints(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y), (x + 2, y), (x - 1, y)]
        self.corners = [(x + 3, y - 1), (x + 3, y + 1), (x + 1, y + 2),
                        (x - 1, y + 2), (x - 2, y + 1), (x - 2, y - 1)]

ALL_SHAPE = []
