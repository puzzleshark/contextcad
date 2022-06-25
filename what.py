import beautifulcad
import beautifulcad.context
import beautifulcad.shapes

import jupyter_cadquery

with beautifulcad.context.Coords("front"):
    b = beautifulcad.shapes.Box(5, 5, 5)


jupyter_cadquery.Part(b._box).show()