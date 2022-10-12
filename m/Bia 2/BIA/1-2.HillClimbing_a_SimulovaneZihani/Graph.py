import matplotlib as matplb
import matplotlib.pyplot as plt
import numpy as np

class Graph:

    # Konstruktor
    def __init__(self, func, interval):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.func = func
        self.interval = interval

    # Zobrazenie grafu
    def Show(self, figName, points = None, points_history = None, interval_anim = 1):
        # Zostavenie bodov pre x a y skrz interval s následným vytvorením meshgridu
        x = y = np.arange(self.interval.lowerBound, self.interval.upperBound, self.interval.step)
        x, y = np.meshgrid(x, y)
        # Vytvorenie krivky grafu danej funkcie
        z = np.array([self.func([x, y]) for x, y in zip(np.ravel(x), np.ravel(y))])
        z = z.reshape(x.shape)

        # Zostavenie grafu pomocou súradnic
        self.ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap=plt.get_cmap('jet'), alpha=0.3)

        # Pomenovanie grafu a jednotlivých os
        self.ax.set_title(figName)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        # Cesta bodov v animaci
        self.path = None
        # Body, ktoré se budú animovat (história priechodov)
        self.points_to_anim = points_history

        # Vykreslenie animácie
        # => vykreslená história priechodov je zobrazená červenou farbou
        if self.points_to_anim != None:
            anim = matplb.animation.FuncAnimation(self.fig, self.anim, len(self.points_to_anim), interval=interval_anim, blit=False, repeat=False)

        # Vykreslenie bodov získaných z vyhľadávacieho algoritmu
        # => výsledné body sú vykreslené zelenou farbou
        if points != None:
            for point in points:
                print(point)
                self.ax.scatter3D(point.x, point.y, point.z, c = '#00ff00')

        plt.show()

    # Vykreslenie animace
    def anim(self, n):
        # Pokiaľ je už vykreslený predchádzajúcizí bod, tak ho odstraň
        if self.path != None:
            self.path.remove()

        # Ak existuje bod pre vykreslenie, tak ho vykresli
        if self.points_to_anim != None:
            self.path = self.ax.scatter3D(self.points_to_anim[n].x, self.points_to_anim[n].y, self.points_to_anim[n].z, c = '#ff0000')