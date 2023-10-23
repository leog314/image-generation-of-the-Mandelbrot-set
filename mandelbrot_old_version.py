import matplotlib.pyplot as plt
import numpy as np

steps = 75

cubic = lambda x: x**2

def mandelbrot(c, func = lambda x: x**2) -> float:
    z = 0
    for step in range(steps):
        if abs(z) > 2:
            return step/steps
        z = func(z) + c
    return 1.

def gen(ncols, nrows, minx, maxx, miny, maxy) -> np.array:
    res = []
    im = maxy
    for col in range(ncols):
        col_li = []
        im -= (maxy + abs(miny))/ncols
        re = minx
        for row in range(nrows):
            c = complex(re, im)
            col_li.append(mandelbrot(c, cubic))
            re += (maxx+abs(minx))/nrows
        col_li = np.array(col_li)
        res.append(col_li)

        print(col) if col % 1000 == 0 else None
    return np.array(res)

data = gen(120, 120, -1.75, 0.5, -1.125, 1.125)

fig, ax = plt.subplots(1, 1)

plt.title("Mandelbrot set")
color = plt.imshow(data, cmap="RdPu")
plt.axis('off')

plt.colorbar(color)
plt.savefig("mandelbrot.png")
plt.show()