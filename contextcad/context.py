import abc

from cadquery import Plane

from contextcad.workbenches import BaseWorkbench, SolidsWorkbench, ShapesWorkbench, LinesWorkbench

import typing as t


class Context(abc.ABC):

    def __init__(self, outer_context: t.Union['Context', None], plane: Plane):
        self.outer_context = outer_context
        self.inner_context = None
        self.active = False

        self.plane = plane

        self.objects = []
        if self.outer_context is not None:
            outer_context.set_for_display(self)

    @abc.abstractmethod
    def workbench(self):
        pass

    def __enter__(self):
        self.active = True
        if self.outer_context is not None:
            self.outer_context.inner_context = self
        return self.workbench()

    def __exit__(self, t, value, traceback):
        self.active = False
        if self.outer_context is not None:
            self.outer_context.inner_context = None

    def current(self):
        if self.active:
            if self.inner_context is None:
                return self
            return self.inner_context.current()
        return self.outer_context.current()
    
    def set_for_display(self, shape):
        self.objects.append(shape)
    
    def _ipython_display_(self):
        if len(self.objects) > 0:
            return self.objects[-1]._ipython_display_()



class SolidsContext(Context):

    def __init__(self, outer_context, plane):
        super().__init__(outer_context, plane)
    
    def workbench(self):
        return SolidsWorkbench(self)



class ShapesContext(Context):

    def __init__(self, outer_context, plane):
        super().__init__(outer_context, plane)

    def workbench(self):
        return ShapesWorkbench(self)

class LinesContext(Context):

    def __init__(self, outer_context, plane):
        super().__init__(outer_context, plane)

    def workbench(self):
        return LinesWorkbench(self)



class BaseContext(Context):

    def build_solids():
        return BaseWorkbench(self)


def workbench():
    return BaseContext(outer_context=None, plane=Plane.named("front"))