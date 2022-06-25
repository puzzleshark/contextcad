# Beautiful Cad


```python
import beautifulcad as bc

with bc.Plane("front"):
    box = bv.Box(5, 5, 5)
    top = box.faces(">Z")
    with bc.Plane(top):
        box -= bc.hole(5)


```