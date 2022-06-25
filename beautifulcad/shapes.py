import jupyter_cadquery
from cadquery import Vector, Plane

from beautifulcad.context import Context
from cadquery.occ_impl.shapes import Solid as CQSolid
from cadquery.occ_impl.shapes import Face as CQFace



class Shape:

    def __init__(self, cq_shape):
        self.ctx = Context.current()
        self._cq_shape = cq_shape.move(self.ctx.plane.location)
    
    def hole(self, diameter, depth):

        boreDir = Vector(0, 0, -1)
        # first make the hole
        h = CQSolid.makeCylinder(
            diameter / 2.0, depth, Vector(), boreDir
        )  # local coordinates!

        new_h = h.moved(Context.current().plane.location)

        return Shape(self._cq_shape.cut(new_h).clean())


    def _ipython_display_(self):
        return jupyter_cadquery.Part(self._cq_shape).show()


class Cylinder(Shape):

    def __init__(self, radius, height):
        super().__init__(CQSolid.makeCylinder(radius, height))


class Box(Shape):

    def __init__(self, l, w, h):
        super().__init__(CQSolid.makeBox(l, w, h))
    
    def faces(self):
        return [Face(f) for f in self._cq_shape.Faces()]


class Face:

    def __init__(self, cq_face: CQFace):
        self.ctx = Context.current()
        self._face = cq_face

    @property
    def plane(self):
        new_context = Context.current()
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

    def _ipython_display_(self):
        return jupyter_cadquery.Part(self._face).show()