
from contextcad.shapes import Circle, Rect


class ShapesWorkbench():

    def __init__(self, ctx):
        self._ctx = ctx
    
    def circle(self, radius):
        return Circle(radius, self._ctx)

    def rect(self, width, height):
        return Rect(width, height, self._ctx)

    def _ipython_display_(self):
        return self._ctx._ipython_display_()
