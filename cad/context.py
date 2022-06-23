import cadquery as cq
import jupyter_cadquery

class Context:

    context_stack = []

    def __enter__(self):
        self.context_stack.append(self)
        return self

    def __exit__(self, t, value, traceback):
        self.context_stack.pop()
    
    @classmethod
    def current(cls):
        return cls.context_stack[-1]



class Part(Context):

    def __init__(self, plane):
        self._cq = cq.Workplane(plane)
        super().__init__()
    
    def _ipython_display_(self):
        return self._cq._ipython_display_()


class CoordiateSystem(Context):
    
    def __init__(self, face):
        self.face = face


class Box:

    def __init__(self, l, w, h):
        ctx = Context.current()
        ctx._cq = ctx._cq.box(l, w, h)
    
    def faces():
        return [0, 1, 2, 3, 4, 5]
    
    def _ipython_display_(self):
        return self._cq._ipython_display_()



class PolyLine:

    def __init__(self):
        pass

    def line(self, x, y):
        pass

    def angle(self, angle, d):
        pass