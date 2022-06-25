from cad.context import Context

import cadquery as cq

from cadquery.occ_impl.shapes import Solid

class Box:

    def __init__(self, l, w, h):
        ctx = Context.current()
        # ctx._cq = ctx._cq.box(l, w, h)
        # self._cq = ctx._cq
        self.box = Solid.makeBox(l, w, h, 0)
    
    def faces(selector):
        return self._cq.faces(selector)
    
    def _ipython_display_(self):
        return self._cq._ipython_display_()


Box(5, 5, 5)