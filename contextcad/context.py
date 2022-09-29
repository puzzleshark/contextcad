import abc

from cadquery import Plane

from contextcad.workbenches import BaseWorkbench, SolidsWorkbench, ShapesWorkbench, LinesWorkbench

import typing as t


class Context(abc.ABC):

    stack = []

    def __init__(self, outer_context: t.Union['Context', None], plane: Plane):
        self.outer_context = outer_context
        self.inner_context = None
        self.active = False

        self.plane = plane

        self.objects = []
        if self.outer_context is not None:
            outer_context.set_for_display(self)

    def __enter__(self):
        self.stack.append(self)
        self.active = True
        if self.outer_context is not None:
            self.outer_context.inner_context = self

    def __exit__(self, t, value, traceback):
        self.stack.pop()
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
    
    def workplane(self):
        if len(self.objects) > 0:
            if isinstance(self.objects[-1], Context):
                return self.objects[-1].workplane()
            return self.objects[-1]

    def _ipython_display_(self):
        if len(self.objects) > 0:
            return self.objects[-1]._ipython_display_()
    
    def _get_description(self):
        if len(self.objects) > 0:
            if isinstance(self.objects[-1], Context):
                return self.objects[-1]._get_description()
            from jupyter_cadquery.utils import numpy_to_json
            from jupyter_cadquery.cad_objects import to_assembly
            from jupyter_cadquery.base import _tessellate_group

            # global json_result
            json_result = numpy_to_json(_tessellate_group(to_assembly(self.objects[-1])))
            return json_result



class SolidsContext(Context):

    def __init__(self, outer_context, plane):
        super().__init__(outer_context, plane)
    

    def __enter__(self):
        super().__enter__()
        return SolidsWorkbench(self)


class ShapesContext(Context):

    def __init__(self, outer_context, plane):
        super().__init__(outer_context, plane)

    def __enter__(self):
        super().__enter__()
        return ShapesWorkbench(self)


class LinesContext(Context):

    def __init__(self, outer_context, plane):
        super().__init__(outer_context, plane)

    def __enter__(self):
        super().__enter__()
        return LinesWorkbench(self)


class BaseContext(Context):

    # def workbench(self):
    #     return BaseWorkbench(self)
    def __enter__(self):
        super().__enter__()
        return BaseWorkbench(self)


def build():
    return BaseContext(outer_context=None, plane=Plane.named("front"))
