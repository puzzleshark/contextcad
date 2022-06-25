import cadquery as cq
import jupyter_cadquery
from cadquery import Plane


class Context:

    context_stack = []

    def __init__(self):
        self.objects = []
        if len(self.context_stack) > 0:
            self.current().add(self)

    def __enter__(self):
        self.context_stack.append(self)
        return self

    def __exit__(self, t, value, traceback):
        self.context_stack.pop()
    
    def add(self, shape):
        self.objects.append(shape)

    
    @classmethod
    def current(cls):
        if len(cls.context_stack) == 0:
            raise ValueError("no beautifulcad context!")
        return cls.context_stack[-1]
    
    def _ipython_display_(self):
        if len(self.objects) > 0:
            ok = self.objects[-1]
            if isinstance(ok, Context):
                return self.objects[-1]._ipython_display_()
            else:
                return ok.show()



class Coords(Context):

    def __init__(self, plane=Plane.named("front")):
        self.plane = plane
        super().__init__()



class PolyLine:

    def __init__(self):
        pass

    def line(self, x, y):
        pass

    def angle(self, angle, d):
        pass