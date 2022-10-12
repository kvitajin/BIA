import matplotlib as matplb
import matplotlib.pyplot as plt
import numpy as np

class Graph:

    # Konstruktor třídy Graph nastavuje základní hodnoty proměnných pro konstrukci vizualizace grafu
    def __init__(self, interval):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.interval = interval

    # Zobrazení grafu
    def Show(self, figName, points = None, points_history = None, interval_anim = 1):
        # Pojmenování grafu a jednotlivých os
        self.ax.set_title(figName)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')

        # Cesta vykreslení v animaci
        self.path = []

        # Cesty, které se budou animovat (historie průchodu)
        self.points_to_anim = []
        for point in points_history:
            for item in point:
                self.points_to_anim.append(item)
        
        # Vykreslení animace
        if self.points_to_anim != None:
            anim = matplb.animation.FuncAnimation(self.fig, self.anim, len(self.points_to_anim), interval=interval_anim, blit=False, repeat=False)


        # Vykreslení měst získaných z vyhledávacího algoritmu
        if points != None:
            for point in points:
                self.ax.scatter(point.x, point.y, c = '#ff0000')
                plt.annotate(point.name, (point.x, point.y), textcoords = "offset points", xytext = (0, 5), ha = 'center')

        plt.show()

    # Vykreslení animace
    def anim(self, n):
        # Vyčištění předchozího vykreslení
        if self.path:
            for i in range(len(self.path)):
                if self.path[i]:
                    self.path[i].pop(0).remove()
        
        # Vykreslení nové cesty
        if self.points_to_anim != None:
            leng = len(self.points_to_anim[n])
            for i in range(leng):
                if i == leng - 1:
                    self.path.append(self.ax.plot([self.points_to_anim[n][i].x, self.points_to_anim[n][0].x], [self.points_to_anim[n][i].y, self.points_to_anim[n][0].y], c = '#ff0000'))
                    continue
                self.path.append(self.ax.plot([self.points_to_anim[n][i].x, self.points_to_anim[n][i + 1].x], [self.points_to_anim[n][i].y, self.points_to_anim[n][i + 1].y], c = '#ff0000'))