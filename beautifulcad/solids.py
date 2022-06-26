import jupyter_cadquery
from cadquery import Vector, Plane

from cadquery.occ_impl.shapes import Solid as CQSolid
from cadquery.occ_impl.shapes import Face as CQFace
import cadquery as cq

import beautifulcad.context



class Solid:

    def __init__(self, wraps, ctx):
        self._ctx = ctx
        self._wraps = wraps
        
        wp = (
            cq.Workplane(self._ctx.plane)
            .add(self._wraps)
        )
        self._ctx.add(wp)
    
    def faces(self, selector=None):
        new_context = self._ctx.current()
        wp = (
            cq.Workplane(new_context.plane)
            .add(self._wraps)
            .faces(selector)
        )
        new_context.add(wp)
        return [Face(f, self, new_context) for f in wp.objects]
    
    def face(self, selector=None):
        faces = self.faces(selector)
        assert len(faces) == 1
        return faces[0]

    def edges(self, selector=None):
        wp = (
            cq.Workplane(self._ctx.current().plane)
            .add(self._wraps)
            .edges(selector)
        )
        self._ctx.current().add(wp)
        return [Edge(e, self, self._ctx.current()) for e in wp.objects]
    
    def hole(self, diameter):
        wp = (
            cq.Workplane(self._ctx.current().plane)
            .add(self._wraps)
            .hole(diameter)
        )
        self._ctx.current().add(wp)
        return wp.objects[0]
    
    def fillet(self, edges, radius):
        wp = (
            cq.Workplane(self._ctx.current().plane)
            .add(self._wraps)
            .add([e._wraps for e in edges])
            .fillet(radius)
        )
        self._ctx.current().add(wp)
        return wp.objects[0]

    def __add__(self, other):
        return Solid(self._wraps.fuse(other._wraps), self._ctx.current())
    
    def __sub__(self, other):
        return Solid(self._wraps.cut(other._wraps), self._ctx.current())


class Cylinder(Solid):

    def __init__(self, height, radius, ctx):
        wp = (
            cq.Workplane(ctx.current().plane)
            .cylinder(height, radius)
        )
        super().__init__(wp.objects[0], ctx)
        # super().__init__(CQSolid.makeCylinder(radius, height), ctx)


class Box(Solid):

    def __init__(self, l, w, h, ctx):
        wp = (
            cq.Workplane(ctx.current().plane)
            .box(l, w, h)
        )
        super().__init__(wp.objects[0], ctx)


class Edge:

    def __init__(self, wraps, parent, ctx):
        self._ctx = ctx
        self._wraps = wraps


    # def solid_workbench(self):
    #     return beautifulcad.context.SolidsContext(outer_context=self.ctx.current(), )

class Vertex:

    def __init__(self, wraps, parent, ctx):
        self._ctx = ctx
        self._wraps = wraps


class Face:

    def __init__(self, wraps, parent, ctx):
        self._ctx = ctx
        self._wraps = wraps


    def edges(self, selector=None):
        current = self._ctx.current()
        wp = (
            cq.Workplane(current.plane)
            .add(self._wraps)
            .edges(selector)
        )
        self._ctx.current().add(wp)
        return [Edge(e, self, current) for e in wp.objects]

    @property
    def plane(self):
        new_context = self._ctx.current()
        return (
            cq.Workplane(new_context.plane)
            .add(self._wraps)
            .workplane(centerOption="CenterOfMass")
            .plane
        )
    
    def solids_workbench(self):
        return beautifulcad.context.SolidsContext(outer_context=self._ctx.current(), plane=self.plane)
    
    def shapes_workbench(self):
        return beautifulcad.context.ShapesContext(outer_context=self._ctx.current(), plane=self.plane)