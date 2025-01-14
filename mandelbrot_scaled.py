import matplotlib.pyplot as plt
import numpy as np
import time
from PIL import Image as im

# Programm für Darstellung des Mandelbrot-Fraktals (ggf. mit Zoom) -> wird durch 3d_mandelbrot.py genutzt

bo: bool = False
maxits: int = 20000 # optional: Legt Maximalwert für Anzahl der Iteration fest

def on_ylims_change(event_ax):
    global bo # Wichtig: da sonst Rekursionsfehler
    if not bo:
        start = time.perf_counter()
        bo = True
        x = event_ax.get_xlim()
        y = event_ax.get_ylim()

        (minx, maxx) = x
        (miny, maxy) = y

        lengthx = man.maxx - man.minx
        lengthy = man.maxy - man.miny
        mxin = man.minx
        myo = man.miny

        man.minx = mxin + lengthx * minx / man.nrow # Umwandlung von minx (Pixelwert) zu entsprechender komplexer Zahl
        man.maxx = mxin + lengthx * maxx / man.nrow
        man.miny = myo + lengthy * (man.ncol - miny) / man.ncol
        man.maxy = man.miny + man.maxx - man.minx

        del myo
        del mxin
        del lengthx
        del lengthy
        del x
        del y

        man.its = man.its + 100 if man.its <= maxits else maxits # Erhöhung der Iterationsanzahl je tiefer man in das Fraktal "hineinblickt"

        data = man.gen()
        event_ax.set_xlim(0, man.nrow)
        event_ax.set_ylim(man.ncol, 0)
        plt.imshow(data, cmap="RdPu")
        print(f"Time needed for image generation: {time.perf_counter() - start}s, Number of iterations used: {man.its}")
        print(man.minx, man.maxx, man.miny, man.maxy)

    else:
        bo = False

class Mandelbrot:
    def __init__(self, max_iters: int=100, pixels: int=1000, minx: float=-2, maxx: float=2, miny: float=-2, maxy: float=2, start_cond: float = 0, func = lambda x: x**2, threshold: float = 2):
        self.its = max_iters
        self.ncol, self.nrow = pixels, pixels
        self.minx, self.maxx, self.miny, self.maxy = minx, maxx, miny, maxy
        self.func = func
        self.t = threshold
        self.cond = start_cond

    def mandelbrot(self, c: complex) -> float:
        z = self.cond
        for step in range(self.its):
            if abs(z) > self.t:
                return 0. # für Farbinterpolation: step / self.its - Für richtige Darstellung von 3d_mandelbrot.py ist hier ein return von 0 notwendig
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

        return np.array(res)

def plot():
    start = time.perf_counter()
    data = man.gen()

    # img = im.fromarray(data)
    # img.save("mandelbrot_16_9.tiff") # speichern der Bilder als .tiff-Datei

    fig, ax = plt.subplots(1, 1)

    plt.title("Mandelbrot-Menge")
    color = plt.imshow(data, cmap="RdPu")
    ax.callbacks.connect('ylim_changed', on_ylims_change)
    plt.axis('off')

    plt.colorbar(color)
    print(f"Time needed for image generation and saving: {time.perf_counter()-start}s, {man.its}")
    # plt.savefig("m_zoom.png", dpi=400)
    plt.show()

man = Mandelbrot()

plot()
