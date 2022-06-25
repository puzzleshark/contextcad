from beautifulcad.context import Context

from cadquery.occ_impl.shapes import Solid
import jupyter_cadquery

class Box:

    def __init__(self, l, w, h):
        ctx = Context.current()
        self._box = Solid.makeBox(l, w, h)
    
    def faces(self, selector):
        return self._cq.faces(selector)
    
    def _ipython_display_(self):
        return jupyter_cadquery.Part(self._box).show()