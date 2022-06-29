# Beautiful Cad


```python
import contextcad

with contextcad.part("front"):
    box = bv.Box(5, 5, 5)
    top = box.faces(">Z")
    with bc.Plane(top):
        box -= bc.hole(5)


```
