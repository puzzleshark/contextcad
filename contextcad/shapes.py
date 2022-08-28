import cadquery as cq
from contextcad.solids import Solid
# from contextcad.workbenches import allow_in_solids_context



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

#   @allow_in_solids_context
    def extrude(self, distance):
        s = cq.Sketch()
        s._faces = self._wraps
        new_context = self._ctx.current()
        wp = (
            cq.Workplane(self._ctx.plane)
            .placeSketch(s)
            .extrude(distance)
        )
        self._ctx.current().set_for_display(s)
        return Solid(wp.objects[0], new_context)


class Circle(Face):

    def __init__(self, radius, ctx):
        current = ctx.current()
        s = (
            cq.Sketch(current.plane)
            .circle(radius)
        )
        ctx.current().set_for_display(s)
        super().__init__(s._faces, ctx)


class Rect(Face):

    def __init__(self, width, height, ctx):
        current = ctx.current()
        s = (
            cq.Sketch(current.plane)
            .rect(width, height)
        )
        ctx.current().set_for_display(s)
        super().__init__(s._faces, ctx)
