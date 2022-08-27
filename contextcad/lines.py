import cadquery as cq
import uuid

class Sketch:
    
    def __init__(self, segments, ctx):
        self._segments = segments
        self._ctx = ctx
        self.constraints = []
    
    def __add__(self, other):
        s = cq.Sketch()
        for seg in self._segments:
            s = s.segment((seg.sx, seg.sy), (seg.ex, seg.ey))
        for seg in other._segments:
            s = s.segment((other.sx, other.sy), (other.ex, other.ey))
        self._ctx.current().set_for_display(s)
        return Sketch([*self._segments, *other._segments], self._ctx)



    def close(self):
        pass

class Line(Sketch):
    
    def __init__(self, sx, sy, ex, ey, ctx):
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        self._ctx = ctx
        self.constraints = []
        self.name = uuid.uuid4()
        super().__init__([self], ctx)
    
    def tangent(self):
        pass
    
    def line(self):
        return UnDirectedLine(self.ex, self.ey, self._ctx)
    
    def arc(self):
        return UnDirectedArc(self.ex, self.ey)

class Arc:
    def __init__(self, sx, sy, mx, my, ex, ey):
        self.sx = sx
        self.sy = sy
        self.mx = mx
        self.my = my
        self.ex = ex
        self.ey = ey


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

    def __init__(self, x, y, ctx):
        self.x = x
        self.y = y
        self._ctx = ctx
        
    def to(self, mx, my, ex, ey):
        return Line(self.x, self.y, x, y)