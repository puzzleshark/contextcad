# Context Cad

Experimental front end for cadquery.

The idea here is the api is a roughly a "direct" api. Meaning when it comes to building an object, that is composed of sub-objects those objects must be explicity referenced and joined. Additionally every object is immutible.

***i.e*** *(to define a union of two solids)*
```
new_shape = a_shape + some_other_shape
```
(`a_shape` and `some_other_shape` remain unchanged)

In this case the magical context only manages the view you see in your cad gui window, and also manages your coordinate system.


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

## `solids_workbench`
Then solids workbench is activated from the current "bench" via 
```
with bench.solids_workbench() as bench:
    # some stuff here
```
## `shapes_workbench`
## `lines_workbench`
## `assembly_workbench` (to-do)
