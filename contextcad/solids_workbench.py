import contextcad.solids



class Moving:

    def translate_3d(x: float, y: float, z: float):
        pass

    def translate_2d(x: float, y: float):
        pass


class SolidsWorkbench:

    def __init__(self, ctx):
        self._ctx = ctx

    def box(self, length, width, height):
            return contextcad.solids.Box(length, width, height, self._ctx)
    
    def _ipython_display_(self):
        return self._ctx._ipython_display_()