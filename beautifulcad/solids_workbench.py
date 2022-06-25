
class SolidsWorkbench():

    def __init__(self, ctx):
        self.ctx = ctx

    def box(self, length, width, height):
            return solids.Box(length, width, height)