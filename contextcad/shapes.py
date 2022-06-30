import cadquery as cq
from contextcad.solids import Solid



class Face:

    def __init__(self, wraps, ctx):
        self._wraps = wraps
        self._ctx = ctx
    
    
    def __add__(self, other):
        combined = self._wraps.fuse(other._wraps)
        s = cq.Sketch()
        s._faces = combined
        self._ctx.current().set_for_display(s)
        return Face(combined, self._ctx.current())

    
    def extrude(self, distance):
        s = cq.Sketch()
        s._faces = self._wraps
        new_context = self._ctx.current()
        wp = (
            cq.Workplane(new_context.plane)
            .placeSketch(s)
            .extrude(distance)
        )
        self._ctx.current().set_for_display(s)
        return Solid(wp.objects[0], new_context)

class Circle(Face):

    def __init__(self, radius, ctx):
        s = (
            cq.Sketch()
            .circle(radius)
        )
        ctx.current().set_for_display(s)
        super().__init__(s._faces, ctx)


class Rect(Face):

    def __init__(self, width, height, ctx):
        s = (
            cq.Sketch()
            .rect(width, height)
        )
        ctx.current().set_for_display(s)
        super().__init__(s._faces, ctx)
