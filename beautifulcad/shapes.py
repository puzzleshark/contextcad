import cadquery as cq



class Face:

    def __init__(self, wraps, ctx):
        self._wraps = wraps
        self._ctx = ctx
    
    
    def __add__(self, other):
        combined = self._wraps.fuse(other._wraps)
        s = cq.Sketch()
        s._faces = combined
        self._ctx.current().add(s)
        return Face(combined, self._ctx)

class Circle(Face):

    def __init__(self, radius, ctx):
        s = (
            cq.Sketch()
            .circle(radius)
        )
        ctx.current().add(s)
        super().__init__(s._faces, ctx)


class Rect(Face):

    def __init__(self, width, height, ctx):
        s = (
            cq.Sketch()
            .rect(width, height)
        )
        ctx.current().add(s)
        super().__init__(s._faces, ctx)
