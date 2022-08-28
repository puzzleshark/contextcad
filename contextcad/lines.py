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

            if isinstance(seg, Line):
                s = s.segment((seg.sx, seg.sy), (seg.ex, seg.ey))
            else:
                s = s.arc((seg.sx, seg.sy), (seg.mx, seg.my), (seg.ex, seg.ey))

        for seg in other._segments:
            if isinstance(seg, Line):
                s = s.segment((other.sx, other.sy), (other.ex, other.ey))
            else:
                s = s.arc((seg.sx, seg.sy), (seg.mx, seg.my), (seg.ex, seg.ey))
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
    
    def angle(self, a):
        return DirectedLine(self.ex, self.ey, a, self._ctx, self)

    def line(self):
        return UnDirectedLine(self.ex, self.ey, self._ctx)
    
    def arc(self):
        return UnDirectedArc(self.ex, self.ey, self._ctx)


class Arc(Sketch):
    def __init__(self, sx, sy, mx, my, ex, ey, ctx):
        self.sx = sx
        self.sy = sy
        self.mx = mx
        self.my = my
        self.ex = ex
        self.ey = ey
        super().__init__([self], ctx)


class Point:

    def __init__(self, x, y, ctx):
        self.x = x
        self.y = y
        self._ctx = ctx

    def line(self):
        return UnDirectedLine(self.x, self.y, self._ctx)
    
    def arc(self):
        return UnDirectedArc(self.x, self.y, self._ctx)


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

    def __init__(self, x, y, a, ctx, parent_line):
        self.x = x
        self.y = y
        self.a = a
        self._ctx = ctx
        self._parent_line = parent_line
        
    def distance(self, d):
        s = (
            cq.Sketch()
            .segment((self._parent_line.sx, self._parent_line.sy), (self._parent_line.ex, self._parent_line.ey), "s1", forConstruction=True) 
            .segment(d, 0, "s2")
            .constrain("s1", "Fixed", None)
            .constrain("s1", "s2", "Coincident", None)
            .constrain("s1", "s2", "Angle", self.a)
            .solve()
        )
        self._ctx.current().set_for_display(s)
                


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
        s = cq.Sketch().arc((self.x, self.y), (mx, my), (ex, ey))
        self._ctx.current().set_for_display(s)
        return Arc(self.x, self.y, mx, my, ex, ey, self._ctx)