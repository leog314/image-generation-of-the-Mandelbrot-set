import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mandelbrot_scaled import Mandelbrot

def it(z0: float, c: complex, k: int) -> float:
    z = z0

    for n in range(k):
        if abs(z)>2:
            return n/k
        z = z**2+c

    return 1.

def gen(pix: int=50, z_min: float=-2, z_max: float=2) -> np.ndarray:
    z_i = z_min
    out = []

    man = Mandelbrot(pixels=pix, minx=-2, maxx=2, miny=-2, maxy=2, start_cond=z_i)
    for pz in range(pix):
        out.append(man.gen())
        z_i += (z_max-z_min)/pix
        print(man.gen())

        man.cond = z_i

    return np.swapaxes(np.stack(out), 0, 2)

pixels = 50
x, y, z = np.indices((pixels, pixels, pixels))

cube = gen(pix=pixels)

colors = plt.cm.RdPu(cube)
print(cube.shape)

ax = plt.figure().add_subplot(projection='3d')
ax.voxels(cube, facecolors=colors)

ax.view_init(90, -90)

ax.set_xlabel("Re(c)")
ax.set_ylabel("Im(c)")
ax.set_zlabel("z_0")

label_all = 10 # pixels % label_all = 0, sonst: Laufzeitfehler

ax.set_xticks(np.arange(0, pixels, step=label_all), labels=[round(-2+4*i/(pixels//label_all), 3) for i in range(pixels//label_all)])
ax.set_yticks(np.arange(0, pixels, step=label_all), labels=[round(-2+4*i/(pixels//label_all), 3) for i in range(pixels//label_all)])
ax.set_zticks(np.arange(0, pixels, step=label_all), labels=[round(-2+4*i/(pixels//label_all), 3) for i in range(pixels//label_all)])

# plt.savefig("mandelbrot@3d_top.png", dpi=400)

plt.show()