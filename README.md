# Context Cad

Experimental front end for cadquery.

```python
import contextcad

with contextcad.solids_workbench("front") as bench:
    box = bench.box(5, 5, 5)
    top = box.face(">Z")
    with top.solids_workbench():
        box_with_hole = box.hole(1)
```

would be analogous to

```python
import cadquery as cq
box_with_hole = (
    cq.Workplane("front")
    .box(5, 5, 5)
    .faces(">Z)
    .hole(1)
)
```

## Introduction

The idea here is the api is a roughly a "direct" api. Meaning when it comes to building an object that is composed of sub-objects, those objects must be explicity referenced. Additionally every object is immutible.

***i.e***  *(to define a union of two solids)*
```python
new_shape = a_shape + some_other_shape
```
(`a_shape` and `some_other_shape` remain unchanged)

The difference between this and a pure "direct" API, is that:
1. There are different contexts (workbenches) which manage different tools you have access to.
2. These context's also live in different coordinate systems.
3. These contexts automatically manage the GUI CAD view.


## Contexts

There are different contexts which supply different APIs.

### `solids_workbench`
The solids workbench is activated from the current "bench" via 
```
with bench.solids_workbench(new_plane) as bench:
    # some stuff here
```

In general it is the context to work with solids.

* Provides methods like `bench.box()`, `bench.sphere()`
* Solids are only allowed to be union'd, insected, etc... in this context
* Shapes are only allowed to be extruded in this context
### `shapes_workbench`

The shapes workbench is activated from the current "bench" via

```
with bench.shapes_workbench(new_plane) as bench:
    # some stuff here
```

* Provides methods like `bench.circle()`, `bench.rect()`
* lines/wires must be "closed" in this context
### `lines_workbench`
haven't quite figured this out but the idea here is this is where you do constraint based sketching

### `assembly_workbench` (to-do)
where you create assemblies

## Control Flow
In cadquery you can have multiple veritices/edges/faces selected and create objects at each point simoltaniously
i.e
```python
import cadquery as cq

box_with_spheres_on_faces = (
    cq.Workplane("front")
    .box(5, 5, 5)
    .faces()
    .sphere(1)
)
```

To reduce complexity, in contextcad this would instead be done with a for loop. Something like
```python
import contextcad

with contextcad.solids_workbench("front") as bench:
    box = bench.box(5, 5, 5)
    box_with_spheres = box
    for face in box.faces():
        box_with_spheres += bench.sphere(1)
```
