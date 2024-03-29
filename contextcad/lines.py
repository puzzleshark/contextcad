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
        return DirectedPoint(self.ex, self.ey, 0, self._ctx, self)
    
    def angle(self, a):
        return DirectedPoint(self.ex, self.ey, a, self._ctx, self)

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
        self._x = x
        self._y = y
        self._ctx = ctx

    def line(self):
        return UnDirectedLine(self._x, self._y, self._ctx)
    
    def arc(self):
        return UnDirectedArc(self._x, self._y, self._ctx)


class UnDirectedLine:

    def __init__(self, x, y, ctx):
        self._x = x
        self._y = y
        self._ctx = ctx
        
    def to(self, x, y):
        s = cq.Sketch().segment((self._x, self._y), (x, y))
        self._ctx.current().set_for_display(s)
        return Line(self._x, self._y, x, y, self._ctx)


class DirectedPoint:

    def __init__(self, x, y, a, ctx, parent_line):
        self._x = x
        self._y = y
        self._a = a
        self._ctx = ctx
        self._parent_line = parent_line
        
    def line(self):
        return DirectedLine(self._x, self._y, self._a, self._ctx, self._parent_line)
    
    def arc(self):
        return DirectedArc(self._x, self._y, self._a, self._ctx, self._parent_line)



class DirectedLine:

    def __init__(self, x, y, a, ctx, parent_line):
        self._x = x
        self._y = y
        self._a = a
        self._ctx = ctx
        self._parent_line = parent_line
        
    def distance(self, d):
        plane = self._ctx.current().plane
        s = (
            cq.Sketch(plane)
            .segment((self._parent_line.sx, self._parent_line.sy), (self._parent_line.ex, self._parent_line.ey), "s1", forConstruction=True) 
            .segment(d, 0, "s2")
            .constrain("s1", "Fixed", None)
            .constrain("s1", "s2", "Coincident", None)
            .constrain("s1", "s2", "Angle", self._a)
            .solve()
        )
        start = plane.toLocalCoords(s._edges[-1].Vertices()[0].Center())
        end = plane.toLocalCoords(s._edges[-1].Vertices()[1].Center())
        s = cq.Sketch().segment((start.x, start.y), (end.x, end.y))
        self._ctx.current().set_for_display(s)
        return Line(start.x, start.y, end.x, end.y, self._ctx)


class DirectedArc:

    def __init__(self, x, y, a, ctx, parent_line):
        self._x = x
        self._y = y
        self._a = a
        self._ctx = ctx
        self._parent_line = parent_line 

    def radius(self, r):
        plane = self._ctx.current().plane
        s = (
            cq.Sketch(plane)
            .segment((self._parent_line.sx, self._parent_line.sy), (self._parent_line.ex, self._parent_line.ey), "s1")
            .arc((self._x, self._y), (self._x + 1, self._y + 1), (self._x + 2, self._y), "a1")
            .constrain("s1", "Fixed", None)
            .constrain("s1", "a1", "Coincident", None)
            .constrain("s1", "a1", "Angle", self._a)
            .constrain("a1", "Radius", r)
            .solve()
        )
        print(s._edges[-1].ShapeType())
        print(dir(s))
        print(dir(s._edges[0]))
        print(s.tag("a1")._solve_status["entities"][1])
        cq.Sketch().arc()
    def to(x, y):
        pass 


class UnDirectedArc:

    def __init__(self, x, y, ctx):
        self.x = x
        self.y = y
        self._ctx = ctx
        
    def to(self, mx, my, ex, ey):
        s = cq.Sketch().arc((self.x, self.y), (mx, my), (ex, ey))
        self._ctx.current().set_for_display(s)
        return Arc(self.x, self.y, mx, my, ex, ey, self._ctx)
