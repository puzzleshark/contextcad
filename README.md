# Context Cad

Experimental front end for cadquery.

The idea here is the api is a roughly a "direct" api. Meaning when it comes to building an object. In this case the magical context only manages the view you see in your cad gui window, and also manages your coordinate system.


```python
import contextcad

with contextcad.part("front") as bench:
    box = bench.box(5, 5, 5)
    top = box.faces(">Z")
    with top.solids_workbench():
        box_with_hole = box.hole(1)


```

# Contexts

There are different contexts which supply different APIs.

* solids_workbench
* shapes_workbench
* lines_workbench
* assembly_workbench (to-do)
