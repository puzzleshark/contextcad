import jupyter_cadquery
from cadquery import Vector, Plane

from cadquery.occ_impl.shapes import Solid as CQSolid
from cadquery.occ_impl.shapes import Face as CQFace
import cadquery as cq



class Solid:

    def __init__(self, cq_shape, ctx, moved=False):
        self.ctx = ctx
        self._cq_shape = cq_shape
        if not moved:
            cq_shape.move(self.ctx.plane.location)
        
        wp = (
            cq.Workplane(self.ctx.plane)
            .add(self._cq_shape)
        )
        self.ctx.add(wp)
    
    def faces(self, selector=None):
        wp = (
            cq.Workplane(self.ctx.current().plane)
            .add(self._cq_shape)
            .faces(selector)
        )
        self.ctx.current().add(wp)
        return [Face(f, self.ctx.current()) for f in wp.objects]
    
    def face(self, selector=None):
        faces = self.faces(selector)
        assert len(faces) == 1
        return faces[0]
    
    def hole(self, diameter):
        wp = (
            cq.Workplane(self.ctx.current().plane)
            .add(self._cq_shape)
            .hole(diameter)
        )
        self.ctx.current().add(wp)
        return wp.objects[0]


    def _ipython_display_(self):
        return jupyter_cadquery.Part(self._cq_shape).show()


class Cylinder(Solid):

    def __init__(self, radius, height, ctx):
        super().__init__(CQSolid.makeCylinder(radius, height), ctx)


class Box(Solid):

    def __init__(self, l, w, h, ctx):
        super().__init__(CQSolid.makeBox(l, w, h), ctx)


class Face:

    def __init__(self, cq_face: CQFace, ctx):
        self.ctx = ctx
        self._face = cq_face

    @property
    def plane(self):
        new_context = self.ctx.current()
        center = self._face.Center()
        normal = self._face.normalAt(center)

        def _computeXdir(normal):
            """
            Figures out the X direction based on the given normal.
            :param :normal The direction that's normal to the plane.
            :type :normal A Vector
            :return A vector representing the X direction.
            """
            xd = Vector(0, 0, 1).cross(normal)
            if xd.Length < 0.01:
                # this face is parallel with the x-y plane, so choose x to be in global coordinates
                xd = Vector(1, 0, 0)
            return xd

        xDir = _computeXdir(normal)


        center = new_context.plane.toLocalCoords(self.ctx.plane.toWorldCoords(center))
        xDir = new_context.plane.toLocalCoords(self.ctx.plane.toWorldCoords(xDir))
        normal = new_context.plane.toLocalCoords(self.ctx.plane.toWorldCoords(normal))

        plane = Plane(center, xDir, normal)

        return plane
    
    def solids_workbench(self):
        pass
        # return SolidsContext(self.plane)

    def _ipython_display_(self):
        return jupyter_cadquery.Part(self._face).show()