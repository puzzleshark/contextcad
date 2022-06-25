import beautifulcad.solids

class SolidsWorkbench():

    def __init__(self, ctx):
        self.ctx = ctx

    def box(self, length, width, height):
            return beautifulcad.solids.Box(length, width, height, self.ctx)
    
    def _ipython_display_(self):
        return self.ctx._ipython_display_()