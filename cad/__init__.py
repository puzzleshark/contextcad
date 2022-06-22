"""
with Part():
    with Extrude(10):
        with Shape():
            # circle(10, l=(0, 10))
            # box()
        circle() + box()

"""


"""
Part(
    Extrude(
        Shape(
            circle(),
            box()
        )
    )
)
"""