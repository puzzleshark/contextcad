import abc

from cadquery import Plane
from solids_workbench import SolidsWorkbench
from shapes_workbench import ShapesWorkbench
from lines_workbench import LinesWorkbench


class Context(abc.ABC):

    def __init__(self, outer_context):
        self.outer_context = outer_context
        self.inner_context = None

        self.objects = []
        if self.outer_context is not None:
            outer_context.add(self)

    @abc.abstractmethod
    def workbench(self):
        pass

    def __enter__(self):
        self.outer_context.inner_context = self
        return self.workbench()

    def __exit__(self, t, value, traceback):
        self.outer_context.inner_context = None

    def current(self):
        if self.outer_context is not None:
            return self.outer_context.current()
        elif self.inner_context is not None:
                return self.inner_context.current()
        else:
            return self
    
    def add(self, shape):
        self.objects.append(shape)
    
    def _ipython_display_(self):
        if len(self.objects) > 0:
            return self.objects[-1]._ipython_display_()



class SolidsContext(Context):

    def __init__(self, outer_context, plane=Plane.named("front")):
        self.plane = plane
        super().__init__(outer_context)
    
    def workbench(self):
        return SolidsWorkbench(self)



class ShapesContext(Context):

    def __init__(self, outer_context):
        super().__init__(outer_context)

    def workbench(self):
        return ShapesWorkbench(self)

class LinesContext(Context):

    def __init__(self, outer_context):
        super().__init__(outer_context)


def solids_workbench(plane: str):
    return SolidsContext(plane)