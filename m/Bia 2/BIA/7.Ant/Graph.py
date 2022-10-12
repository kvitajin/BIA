import matplotlib as matplb
import matplotlib.pyplot as plt
import numpy as np

class Graph:

    # Konstruktor triedy Graph nastavuje základne hodnoty premenných pre konstrukciu vizualizacie grafu
    def __init__(self, interval):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.interval = interval

    # Zobrazenie grafu
    def Show(self, figName, points = None, points_history = None, interval_anim = 1):
        # Pomenovanie grafu a jednotlivých os
        self.ax.set_title(figName)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')

        # Cesta vykreslenia v animacii
        self.path = []

        # Cesty, ktoré se budu animovat (historie priechodov)
        self.points_to_anim = []
        for point in points_history:
            for item in point:
                self.points_to_anim.append(item)
        
        # Vykreslenie animacie
        if self.points_to_anim != None:
            anim = matplb.animation.FuncAnimation(self.fig, self.anim, len(self.points_to_anim), interval=interval_anim, blit=False, repeat=False)


        # Vykreslenie mest získaných z vyhladávacieho algoritmu
        if points != None:
            for point in points:
                self.ax.scatter(point.x, point.y, c = '#ff0000')
                plt.annotate(point.name, (point.x, point.y), textcoords = "offset points", xytext = (0, 5), ha = 'center')

        plt.show()

    # Vykreslenie animacie
    def anim(self, n):
        # Vyčištenie predchadzajúceho vykreslenia
        if self.path:
            for i in range(len(self.path)):
                if self.path[i]:
                    self.path[i].pop(0).remove()
        
        # Vykreslenie novej cesty
        if self.points_to_anim != None:
            leng = len(self.points_to_anim[n].path)
            for i in range(leng):
                if i == leng - 1:
                    self.path.append(self.ax.plot([self.points_to_anim[n].path[i].x, self.points_to_anim[n].path[0].x], [self.points_to_anim[n].path[i].y, self.points_to_anim[n].path[0].y], c = '#ff0000'))
                    continue
                self.path.append(self.ax.plot([self.points_to_anim[n].path[i].x, self.points_to_anim[n].path[i + 1].x], [self.points_to_anim[n].path[i].y, self.points_to_anim[n].path[i + 1].y], c = '#ff0000'))