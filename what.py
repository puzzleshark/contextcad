import cad.context

#%%

with cad.context.Coords("front"):
    print(cad.context.Context.context_stack)
    print("hi")
    cad.context.Box(5, 5, 5)
# %%
