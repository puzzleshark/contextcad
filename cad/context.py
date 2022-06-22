

class Context:

    context_stack = []

    def __init__(self):
        pass

    def __enter__(self):
        self.context_stack.append(self)

    def __exit__(self, t, value, traceback):
        print(t, value, traceback)
        self.context_stack.pop()



class CoordiateSystem(Context):
    
    def __init__(self, face):
        self.face = face


class Box:

    def __init__(self, l, w, h):
        self.l = l
        self.w = w
        self.h = h
    
    def faces():
        return [0, 1, 2, 3, 4, 5]



class PolyLine:

    def __init__(self):
        pass

    def line(self, x, y):
        pass

    def angle(self, angle, d):
        pass

    



with Context():
    with Context():
        ok = 1

print(ok)