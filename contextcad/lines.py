import cadquery as cq

class Sketch:
    
    def __init__(self, segments, ctx):
        self._segments = segments
        self._ctx = ctx
        self.segments = []
    
    def __add__(self, other):
        return Sketch([*self.segments, other], self._ctx)


    def close(self):
        pass

class Line:
    
    def __init__(self, sx, sy, ex, ey, ctx):
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        self._ctx = ctx
    
    def tangent(self):
        pass

class Arc:
    def __init__(self, sx, sy, ex, ey, r):
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        self.r = r


class Point:

    def __init__(self, x, y, ctx):
        self.x = x
        self.y = y
        self._ctx = ctx

    def line(self):
        return UnDirectedLine(self.x, self.y, self._ctx)
    
    def arc(self):
        return UnDirectedArc(self.x, self.y)


class UnDirectedLine:

    def __init__(self, x, y, ctx):
        self.x = x
        self.y = y
        self._ctx = ctx
        
    def to(self, x, y):
        s = cq.Sketch().segment((self.x, self.y), (x, y))
        self._ctx.current().set_for_display(s)
        return Line(self.x, self.y, x, y, self._ctx)


class DirectedLine:

    def __init__(self, x, y, a):
        self.x = x
        self.y = y
        self.a = a


class DirectedArc:

    def __init__(self, x, y, a):
        self.x = x
        self.y = y
        self.a = a


class UnDirectedArc:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def to(self, x, y):
        return Line(self.x, self.y, x, y)