import jupyter_cadquery
from cadquery import Vector, Plane

from cadquery.occ_impl.shapes import Solid as CQSolid
from cadquery.occ_impl.shapes import Face as CQFace
import cadquery as cq

import contextcad.context



class Solid:

    def __init__(self, wraps, ctx):
        self._ctx = ctx
        self._wraps = wraps
        
        wp = (
            cq.Workplane(self._ctx.plane)
            .add(self._wraps)
        )
        self._ctx.set_for_display(wp)
    
    def faces(self, selector=None):
        current = self._ctx.current()
        wp = (
            cq.Workplane(current.plane)
            .add(self._wraps)
            .faces(selector)
        )
        current.set_for_display(wp)
        return [Face(f, self, current) for f in wp.objects]
    
    def face(self, selector=None):
        faces = self.faces(selector)
        assert len(faces) == 1
        return faces[0]

    def edges(self, selector=None):
        current = self._ctx.current()
        wp = (
            cq.Workplane(current.plane)
            .add(self._wraps)
            .edges(selector)
        )
        current.set_for_display(wp)
        return [Edge(e, self, current) for e in wp.objects]
    
    def hole(self, diameter):
        current = self._ctx.current()
        wp = (
            cq.Workplane(current.plane)
            .add(self._wraps)
            .hole(diameter)
        )
        current.set_for_display(wp)
        return Solid(wp.objects[0], current)
    
    def fillet(self, edges, radius):
        current = self._ctx.current()
        wp = (
            cq.Workplane(current.plane)
            .add(self._wraps)
            .add([e._wraps for e in edges])
            .fillet(radius)
        )
        current.set_for_display(wp)
        return Solid(wp.objects[0], current)

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


class Box(Solid):

    def __init__(self, l, w, h, ctx):
        wp = (
            cq.Workplane(ctx.current().plane)
            .box(l, w, h)
        )
        super().__init__(wp.objects[0], ctx)


class Edge:

    def __init__(self, wraps, parent, ctx):
        self._wraps = wraps
        self._parent = parent
        self._ctx = ctx



class Vertex:

    def __init__(self, wraps, parent, ctx):
        self._wraps = wraps
        self._parent = parent
        self._ctx = ctx


class Face:

    def __init__(self, wraps, parent, ctx):
        self._wraps = wraps
        self._parent = parent
        self._ctx = ctx


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
    
    def build3d(self):
        return contextcad.context.SolidsContext(outer_context=self._ctx.current(), plane=self.plane)
    
    def build2d(self):
        return contextcad.context.ShapesContext(outer_context=self._ctx.current(), plane=self.plane)