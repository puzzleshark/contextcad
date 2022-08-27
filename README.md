# Context Cad

Experimental front end for cadquery.

```python
import contextcad

with contextcad.workbench() as bench:
    with bench.build3d() as b:
        box = bench.box(5, 5, 5)
        top = box.face(">Z")
        with top.build3d():
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

The idea here is the api is a roughly a *"direct"* api. Meaning when it comes to building an object that is composed of sub-objects, those sub-objects must be explicity referenced. Additionally every object is **immutable**.

***i.e***  *(to define a union of two solids)*
```python
new_shape = a_shape + some_other_shape
```
(`a_shape` and `some_other_shape` remain unchanged)

The difference between this and a pure "direct" API, is that:
1. There are different contexts which manage different tools you have access to.
2. Each context lives on a plane, which sets the local coordinate system.
3. These contexts automatically manage the GUI CAD view.


## Contexts

There are different contexts which supply different APIs.

### `build3d`
The build3d context is activated from the current context via 
```
with c.build3d() as c:
    # some stuff here
```

In general it is the context to work with solids.

* Provides methods like `c.box()`, `c.sphere()`
* Solids are only allowed to be union'd, insected, etc... in this context
* Shapes are only allowed to be extruded in this context
### `build2d`

The shapes workbench is activated from the current context via

```
with c.build2d() as c:
    # some stuff here
```

* Provides methods like `c.circle()`, `c.rect()`
* lines/wires must be "closed" in this context
### `lines_workbench`
haven't quite figured this out but the idea here is this is where you do constraint based sketching

### `assembly_workbench` (to-do)
where you create assemblies

## Control Flow
In cadquery you can have multiple veritices/edges/faces selected and create objects at each point simultaneously
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

with contextcad.workbench() as bench:
    with bench.build3d() as b:
        box = b.box(5, 5, 5)
        box_with_spheres = box
        for face in box.faces():
            with face.build3d() as b:  # plane is automatically set to the face's plane
                box_with_spheres += bench.sphere(1)
```

```python
with build1d() as ctx:
    l = ctx.start(0, 0).line(5, 0)
    l += l.angle(90).line(5)
```

```python
with build1d() as ctx:
    ctx.line(0,3).angle(30).go().until(4)
    ctx.go().parallel_to().go().until(4)
```