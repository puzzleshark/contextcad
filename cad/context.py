import cadquery as cq

class Context:

    context_stack = []

    def __init__(self):
        pass

    def __enter__(self):
        self.context_stack.append(self)

    def __exit__(self, t, value, traceback):
        print(t, value, traceback)
        self.context_stack.pop()
    
    @classmethod
    def current(cls):
        return cls.context_stack[-1]



class Part(Context):

    def __init__(self, plane = "front" | "back" | "right" | "left" | "top" | "bottom"):
        self._cq = cq.Workplane(plane)







class CoordiateSystem(Context):
    
    def __init__(self, face):
        self.face = face


class Box:

    def __init__(self, l, w, h):
        ctx = Context.current()
        self._cq = ctx.box(l, w, h)
    
    def faces():
        return [0, 1, 2, 3, 4, 5]



class PolyLine:

    def __init__(self):
        pass

    def line(self, x, y):
        pass

    def angle(self, angle, d):
        pass