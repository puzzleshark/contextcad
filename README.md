# Beautiful Cad


```python
import contextcad

with contextcad.part("front") as bench:
    box = bench.box(5, 5, 5)
    top = box.faces(">Z")
    with top.solids_workbench():
        box_with_hole = box.hole(1)


```
