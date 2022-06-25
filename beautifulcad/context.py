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
        if len(cls.context_stack) == 0:
            raise ValueError("no beautifulcad context!")
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



class PolyLine:

    def __init__(self):
        pass

    def line(self, x, y):
        pass

    def angle(self, angle, d):
        pass