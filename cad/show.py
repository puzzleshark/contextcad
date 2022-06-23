import jupyter_cadquery


def show(model):
    from jupyter_cadquery.utils import numpy_to_json
    from jupyter_cadquery.cad_objects import to_assembly
    from jupyter_cadquery.base import _tessellate_group

    global json_result
    json_result = numpy_to_json(_tessellate_group(to_assembly(model)))




import cadquery as cq


box = cq.Workplane().box(5, 5, 5)

show(box)