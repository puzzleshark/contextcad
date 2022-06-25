# Beautiful Cad


```python
import beautifulcad as bc

with bc.Plane("front"):
    box = bv.Box(5, 5, 5)
    top = box.faces(">Z")
    with bc.Plane(top):
        box -= bc.hole(5)


```



```python
import cadquery as cq

with cq.solids_workbench("front") as bench:
    box = bench.box(7, 8, 3)
    top = b.faces(">Z")
    top_edges = top.edges()
    chamfered_box = top_edges.chamfer(1)
    


```