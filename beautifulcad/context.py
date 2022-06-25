import cadquery as cq
import jupyter_cadquery
from cadquery import Plane

import beautifulcad.solids as solids


class Context():

    def __init__(self, outer_context):
        self.outer_context = outer_context
        self.inner_context = None

        self.objects = []
        if len(self.context_stack) > 0:
            outer_context.add(self)

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

    
    @classmethod
    def current(cls):
        if len(cls.context_stack) == 0:
            raise ValueError("no beautifulcad context!")
        return cls.context_stack[-1]
    
    def _ipython_display_(self):
        if len(self.objects) > 0:
            return self.objects[-1]._ipython_display_()



class SolidsContext(Context):

    def __init__(self, outer_context, plane=Plane.named("front")):
        self.plane = plane
        super().__init__(outer_context)
    
    def workbench():
        return SolidsWorkbench()



class ShapesContext(Context):

    def __init__(self, outer_context):
        super().__init__(outer_context)

class LinesContext(Context):

    def __init__(self, outer_context):
        super().__init__(outer_context)


def solids_workbench(plane: str):
    return SolidsContext(plane)