def g(x):
    yield from range(x, 0, -1)
    yield from range(x)
     
list(g(5))
#[5, 4, 3, 2, 1, 0, 1, 2, 3, 4]