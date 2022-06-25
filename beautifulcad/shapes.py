from beautifulcad.context import Context, Coords

import cadquery as cq

from cadquery.occ_impl.shapes import Solid

class Box:

    def __init__(self, l, w, h):
        ctx = Context.current()
        # ctx._cq = ctx._cq.box(l, w, h)
        # self._cq = ctx._cq
        self._box = Solid.makeBox(l, w, h)
    
    def faces(self, selector):
        return self._cq.faces(selector)
    
    def _ipython_display_(self):
        return self._cq._ipython_display_()

with Coords("front"):
    Box(5, 5, 5)