
from beautifulcad.shapes import Circle, Rect


class ShapesWorkbench():

    def __init__(self, ctx):
        self.ctx = ctx
    
    def circle(self, radius):
        return Circle(radius, self.ctx)

    def rect(self, width, height):
        return Rect(width, height, self.ctx)

    def _ipython_display_(self):
        return self.ctx._ipython_display_()
