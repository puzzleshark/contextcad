import jupyter_cadquery
from cadquery import Vector, Plane

from cadquery.occ_impl.shapes import Solid as CQSolid
from cadquery.occ_impl.shapes import Face as CQFace
import cadquery as cq

import beautifulcad.context



class Solid:

    def __init__(self, wraps, ctx, moved=False):
        self.ctx = ctx
        self._wraps = wraps
        if not moved:
            wraps.move(self.ctx.plane.location)
        
        wp = (
            cq.Workplane(self.ctx.plane)
            .add(self._wraps)
        )
        self.ctx.add(wp)
    
    def faces(self, selector=None):
        wp = (
            cq.Workplane(self.ctx.current().plane)
            .add(self._wraps)
            .faces(selector)
        )
        self.ctx.current().add(wp)
        return [Face(f, self, self.ctx.current()) for f in wp.objects]
    
    def face(self, selector=None):
        faces = self.faces(selector)
        assert len(faces) == 1
        return faces[0]

    def edges(self, selector=None):
        wp = (
            cq.Workplane(self.ctx.current().plane)
            .add(self._wraps)
            .edges(selector)
        )
        self.ctx.current().add(wp)
        return [Edge(e, self, self.ctx.current()) for e in wp.objects]
    
    def hole(self, diameter):
        wp = (
            cq.Workplane(self.ctx.current().plane)
            .add(self._wraps)
            .hole(diameter)
        )
        self.ctx.current().add(wp)
        return wp.objects[0]


class Cylinder(Solid):

    def __init__(self, radius, height, ctx):
        super().__init__(CQSolid.makeCylinder(radius, height), ctx)


class Box(Solid):

    def __init__(self, l, w, h, ctx):
        super().__init__(CQSolid.makeBox(l, w, h), ctx)


class Edge:

    def __init__(self, wraps, parent, ctx):
        self.ctx = ctx
        self._wraps = wraps

class Vertex:

    def __init__(self, wraps, parent, ctx):
        self.ctx = ctx
        self._wraps = wraps


class Face:

    def __init__(self, cq_face: CQFace, ctx):
        self.ctx = ctx
        self._face = cq_face


    def edges(self, selector=None):
        wp = (
            cq.Workplane(self.ctx.current().plane)
            .add(self._cq_shape)
            .edges(selector)
        )
        self.ctx.current().add(wp)
        return [Edge(e, self.ctx.current()) for e in wp.objects]

    @property
    def plane(self):
        new_context = self.ctx.current()
        return (
            cq.Workplane(new_context.plane)
            .add(self._face)
            .workplane()
            .plane
        )


        # center = self._face.Center()
        # normal = self._face.normalAt(center)

        # def _computeXdir(normal):
        #     """
        #     Figures out the X direction based on the given normal.
        #     :param :normal The direction that's normal to the plane.
        #     :type :normal A Vector
        #     :return A vector representing the X direction.
        #     """
        #     xd = Vector(0, 0, 1).cross(normal)
        #     if xd.Length < 0.01:
        #         # this face is parallel with the x-y plane, so choose x to be in global coordinates
        #         xd = Vector(1, 0, 0)
        #     return xd

        # xDir = _computeXdir(normal)


        # center = new_context.plane.toLocalCoords(self.ctx.plane.toWorldCoords(center))
        # xDir = new_context.plane.toLocalCoords(self.ctx.plane.toWorldCoords(xDir))
        # normal = new_context.plane.toLocalCoords(self.ctx.plane.toWorldCoords(normal))

        # plane = Plane(center, xDir, normal)

        # return plane
    
    def solids_workbench(self):
        return beautifulcad.context.SolidsContext(outer_context=self.ctx.current(), plane=self.plane)