import matplotlib.pyplot as plt
import numpy as np

bo: bool = False

def on_ylims_change(event_ax):
    global bo
    if not bo:
        bo = True
        x = event_ax.get_xlim()
        y = event_ax.get_ylim()

        (minx, maxx) = x
        (miny, maxy) = y

        lengthx = man.maxx - man.minx
        lengthy = man.maxy - man.miny
        mxin = man.minx
        myo = man.miny

        man.minx = mxin + lengthx * minx / man.nrow
        man.maxx = mxin + lengthx * maxx / man.nrow
        man.miny = myo + lengthy * (man.ncol - miny) / man.ncol
        man.maxy = man.miny + man.maxx - man.minx

        data = man.gen()
        event_ax.set_xlim(0, man.nrow)
        event_ax.set_ylim(man.ncol, 0)
        plt.imshow(data, cmap="RdPu")

    else:
        bo = False

class Mandelbrot:
    def __init__(self, max_iters: int=100, pixels: int=720, minx: float=-2, maxx: float=2, miny: float=-2, maxy: float=2, func = lambda x: x**2, threshold: float = 2):
        self.its = max_iters
        self.ncol, self.nrow = pixels, pixels
        self.minx, self.maxx, self.miny, self.maxy = minx, maxx, miny, maxy
        self.func = func
        self.t = threshold
    def mandelbrot(self, c: complex) -> float:
        z = c
        for step in range(self.its):
            if abs(z) > self.t:
                return step / self.its
            z = self.func(z) + c
        return 1.

    def gen(self) -> np.array:
        res = []
        im = self.maxy
        for col in range(self.ncol):
            col_li = []
            im -= (self.maxy - self.miny) / self.ncol
            re = self.minx
            for row in range(self.nrow):
                c = complex(re, im)
                col_li.append(self.mandelbrot(c))
                re += (self.maxx - self.minx) / self.nrow
            col_li = np.array(col_li)
            res.append(col_li)

            # print(col) if col % 1000 == 0 else None
        return np.array(res)

man = Mandelbrot()

def plot():
    data = man.gen()
    fig, ax = plt.subplots(1, 1)

    plt.title("Mandelbrot set")
    color = plt.imshow(data, cmap="RdPu")
    ax.callbacks.connect('ylim_changed', on_ylims_change)
    plt.axis('off')

    plt.colorbar(color)
    plt.show()

plot()
