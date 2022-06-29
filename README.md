# Context Cad

Experimental front end for cadquery.

```python
import contextcad

with contextcad.part("front") as bench:
    box = bench.box(5, 5, 5)
    top = box.faces(">Z")
    with top.solids_workbench():
        box_with_hole = box.hole(1)


```

## Introduction

The idea here is the api is a roughly a "direct" api. Meaning when it comes to building an object that is composed of sub-objects, those objects must be explicity referenced. Additionally every object is immutible.

***i.e***  *(to define a union of two solids)*
```python
new_shape = a_shape + some_other_shape
```
(`a_shape` and `some_other_shape` remain unchanged)

The difference between this and a pure "direct" API, is that:
1. There are different contexts (workbenches) which manage different tools you have access to
2. These context's also live in different coordinate systems.
3. These contexts manage the GUI CAD view.
In this case the magical context only manages the view you see in your cad gui window, and also manages your coordinate system.


## Contexts

There are different contexts which supply different APIs.

### `solids_workbench`
The solids workbench is activated from the current "bench" via 
```
with bench.solids_workbench() as bench:
    # some stuff here
```

It provides methods like `bench.box()`, `bench.sphere()`, additionally shapes are only allowed to be extruded in this context.
### `shapes_workbench`

The shapes workbench is activated from the current "bench" via

```
with bench.shapes_workbench() as bench:
    # some stuff here
```

It provides methods like `bench.circle(), `bench.rect()`, additionally lines/wires must be "closed" in this context.
### `lines_workbench`

### `assembly_workbench` (to-do)
