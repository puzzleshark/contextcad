import contextcad.solids
import contextcad.shapes
import contextcad.lines
import contextcad.context

from cadquery import Plane



class PlaneMovement2d:

    # def translate_3d(x: float, y: float, z: float):
    #     pass

    def translate_2d(x: float, y: float):
        pass


class BaseWorkbench:

    def __init__(self, ctx):
        self._ctx = ctx

    def build3d(self):
        return contextcad.context.SolidsContext(Plane.named("front"))
    
    def build2d(self):
        return contextcad.context.ShapesContext(Plane.named("front"))
    
    def build1d(self):
        return contextcad.context.LinesContext(Plane.named("front"))



class SolidsWorkbench:

    def __init__(self, ctx):
        self._ctx = ctx

    def box(self, length, width, height):
            return contextcad.solids.Box(length, width, height, self._ctx)
    
    def _ipython_display_(self):
        return self._ctx._ipython_display_()



class ShapesWorkbench:

    def __init__(self, ctx):
        self._ctx = ctx
    
    def circle(self, radius):
        return contextcad.shapes.Circle(radius, self._ctx)

    def rect(self, width, height):
        return contextcad.shapes.Rect(width, height, self._ctx)

    def _ipython_display_(self):
        return self._ctx._ipython_display_()


class LinesWorkbench():

    def __init__(self, ctx):
        self.ctx = ctx


    # lines
    
    def line(start, finish):
        pass

    def tangent():
        pass

    def parallel():
        pass