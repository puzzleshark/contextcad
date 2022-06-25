import beautifulcad
import beautifulcad.context
import beautifulcad.shapes


with beautifulcad.context.SolidsContext():
    b = beautifulcad.shapes.Box(5, 5, 5)
    faces = b.faces()
    with beautifulcad.context.SolidsContext(faces[0].plane):
        bh = b.hole(3, 3)