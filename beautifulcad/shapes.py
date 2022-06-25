import jupyter_cadquery
from cadquery import Vector, Plane

from beautifulcad.context import Context
from cadquery.occ_impl.shapes import Solid as CQSolid
from cadquery.occ_impl.shapes import Face as CQFace

class Box:

    def __init__(self, l, w, h):
        self.ctx = Context.current()
        self._box = CQSolid.makeBox(l, w, h)
    
    def faces(self):
        return [Face(f) for f in self._box.Faces()]
    
    def _ipython_display_(self):
        return jupyter_cadquery.Part(self._box).show()


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
            if xd.Length < self.ctx.tolerance:
                # this face is parallel with the x-y plane, so choose x to be in global coordinates
                xd = Vector(1, 0, 0)
            return xd

        xDir = _computeXdir(normal)

        plane = Plane(center, xDir, normal)

        return plane

    def _ipython_display_(self):
        return jupyter_cadquery.Part(self._face).show()