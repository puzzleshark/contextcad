import cadquery as cq
import jupyter_cadquery
from cadquery import Plane


class Context:

    context_stack = []

    def __init__(self):
        self.objects = []

    def __enter__(self):
        self.context_stack.append(self)
        return self

    def __exit__(self, t, value, traceback):
        self.context_stack.pop()
    
    def add(shape):
        self.objects.append(shape)

    
    @classmethod
    def current(cls):
        if len(cls.context_stack) == 0:
            raise ValueError("no beautifulcad context!")
        return cls.context_stack[-1]
    
    def _ipython_display_(self):
        return self.current().objects[-1]._ipython_display_()



class Coords(Context):

    def __init__(self, plane=Plane.named("front")):
        self.plane = plane
        super().__init__()
    
    # def _ipython_display_(self):
        # return self._cq._ipython_display_()



class PolyLine:

    def __init__(self):
        pass

    def line(self, x, y):
        pass

    def angle(self, angle, d):
        pass