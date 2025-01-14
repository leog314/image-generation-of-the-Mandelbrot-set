import matplotlib.pyplot as plt
import numpy as np
import time
from PIL import Image as im
import multiprocessing as mp

# Berechnung des Mandelbrot-Fraktals für CPU mit 8 Kernen

data1 = []
data2 = []
data3 = []
data4 = []
data5 = []
data6 = []
data7 = []
data8 = []

def mandelbrot(c, func = lambda x: x**2) -> float:
    steps: int = 100
    z = 0
    for step in range(steps):
        if abs(z) > 2:
            return step/steps
        z = func(z) + c
    return 1.

def gen(ncols: int, nrows: int, xmi: float, xma: float, ymi: float, yma: float, res: list) -> None:
    im = yma
    for col in range(ncols):
        col_li = []
        im -= (yma -ymi) / ncols
        re = xmi
        for row in range(nrows):
            c = complex(re, im)
            col_li.append(mandelbrot(c))
            re += (xma - xmi) / nrows
        col_li = np.array(col_li)
        res.append(col_li)

if __name__=="__main__":
    # define global variables
    minx, maxx, miny, maxy = -1.5, 0.5, -1, 1
    pixel: int = 1024 # -> pixel % 8 = 0 (!)

    dy = (maxy-miny)/8

    manager = mp.Manager()
    data1 = manager.list()
    data2 = manager.list()
    data3 = manager.list()
    data4 = manager.list()
    data5 = manager.list()
    data6 = manager.list()
    data7 = manager.list()
    data8 = manager.list()

    start = time.perf_counter()

    task1 = mp.Process(target=gen, args=(pixel//8, pixel, minx, maxx, maxy-dy, maxy, data1,))
    task2 = mp.Process(target=gen, args=(pixel//8, pixel, minx, maxx, maxy-2*dy, maxy-dy, data2,))
    task3 = mp.Process(target=gen, args=(pixel//8, pixel, minx, maxx, maxy-3*dy, maxy-2*dy, data3,))
    task4 = mp.Process(target=gen, args=(pixel//8, pixel, minx, maxx, maxy-4*dy, maxy-3*dy, data4,))
    task5 = mp.Process(target=gen, args=(pixel//8, pixel, minx, maxx, maxy-5*dy, maxy-4*dy, data5,))
    task6 = mp.Process(target=gen, args=(pixel//8, pixel, minx, maxx, maxy-6*dy, maxy-5*dy, data6,))
    task7 = mp.Process(target=gen, args=(pixel//8, pixel, minx, maxx, maxy-7*dy, maxy-6*dy, data7,))
    task8 = mp.Process(target=gen, args=(pixel//8, pixel, minx, maxx, maxy-8*dy, maxy-7*dy, data8,))

    task1.start()
    task2.start()
    task3.start()
    task4.start()
    task5.start()
    task6.start()
    task7.start()
    task8.start()

    task1.join()
    task2.join()
    task3.join()
    task4.join()
    task5.join()
    task6.join()
    task7.join()
    task8.join()

    data1 = list(data1)
    data2 = list(data2)
    data3 = list(data3)
    data4 = list(data4)
    data5 = list(data5)
    data6 = list(data6)
    data7 = list(data7)
    data8 = list(data8)

    data = np.array(data1 + data2 + data3 + data4 + data5 + data6 + data7 + data8)
    # print(data, data.shape)

    fig, ax = plt.subplots(1, 1)

    plt.title("Die Mandelbrot-Menge")
    color = plt.imshow(data, cmap="RdPu")
    plt.axis('off')
    # ax.callbacks.connect('ylim_changed', on_ylims_change)

    plt.colorbar(color)
    print(f"Time needed for image generation: {time.perf_counter() - start}s")

    plt.savefig("sharp_mandelbrot.png", dpi=500)
    plt.show()

    # im_data = im.fromarray(data)

    # im_data.save("mandelbrot.tiff")
