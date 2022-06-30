import functools

import contextcad.solids
import contextcad.shapes
import contextcad.lines
import contextcad.context

from cadquery import Plane

def active(fn):
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        if self._ctx.active is False or self._ctx.inner_context is not None:
            raise ValueError("not current context!")
        return fn(self, *args, **kwargs)
    return wrapper


# class PlaneMovement2d:

#     def translate_3d(x: float, y: float, z: float):
#         pass

#     def translate_2d(x: float, y: float):
#         pass


class BaseWorkbench:

    def __init__(self, ctx):
        self._ctx = ctx

    @active
    def build3d(self):
        return contextcad.context.SolidsContext(self._ctx, Plane.named("front"))
    
    @active
    def build2d(self):
        return contextcad.context.ShapesContext(self._ctx, Plane.named("front"))
    
    @active
    def build1d(self):
        return contextcad.context.LinesContext(self._ctx, Plane.named("front"))

    def _ipython_display_(self):
        return self._ctx._ipython_display_()



class SolidsWorkbench:

    def __init__(self, ctx):
        self._ctx = ctx


    @active
    def box(self, length, width, height):
            return contextcad.solids.Box(length, width, height, self._ctx)
    
    def _ipython_display_(self):
        return self._ctx._ipython_display_()



class ShapesWorkbench:

    def __init__(self, ctx):
        self._ctx = ctx
    
    @active
    def circle(self, radius):
        return contextcad.shapes.Circle(radius, self._ctx)

    @active
    def rect(self, width, height):
        return contextcad.shapes.Rect(width, height, self._ctx)

    def _ipython_display_(self):
        return self._ctx._ipython_display_()


class LinesWorkbench():

    def __init__(self, ctx):
        self.ctx = ctx


    # lines
    
    @active
    def line(start, finish):
        pass

    @active
    def tangent():
        pass

    @active
    def parallel():
        pass