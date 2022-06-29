import beautifulcad.solids

class SolidsWorkbench():

    def __init__(self, ctx):
        self._ctx = ctx

    def box(self, length, width, height):
            return beautifulcad.solids.Box(length, width, height, self._ctx)
    
    def _ipython_display_(self):
        return self._ctx._ipython_display_()