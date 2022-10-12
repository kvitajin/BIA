import matplotlib as matplb
import matplotlib.pyplot as plt
import numpy as np

class Graph:

    # Konstruktor triedy Graph nastavuje základne hodnoty premenných pre konstrukciu vizualizacie grafu
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

        # Zostavenie grafu pomocou suradnic
        self.ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap=plt.get_cmap('jet'), alpha=0.3)

        # Pomenovánie grafu a jednotlivých os
        self.ax.set_title(figName)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        # Cesta bodov v animacii
        self.path = None
        # Body, ktoré sa budu animovat (historie priechodov)
        self.points_to_anim = points_history

        # Vykreslenie animacee
        # => vykreslená historia priechodu je zobrazena červenou
        if self.points_to_anim != None:
            anim = matplb.animation.FuncAnimation(self.fig, self.anim, len(self.points_to_anim), interval=interval_anim, blit=False, repeat=False)

        # Vykreslenie bodov získaných z vyhledávacieho algoritmu
        # => výsledné body su vykreslene zelenou
        if points != None:
            for point in points:
                self.ax.scatter3D(point.x, point.y, point.z, c = '#00ff00')

        plt.show()

    # Zobrazenie grafu vrátane vykreslenia historie priechodov celej populacie
    def ShowByPopulation(self, figName, best_individual = None, population_history = None, interval_anim = 1):
        # Zostavenie bodov pre x a y skrz interval s následným vytvorením meshgridu
        x = y = np.arange(self.interval.lowerBound, self.interval.upperBound, self.interval.step)
        x, y = np.meshgrid(x, y)
        # Vytvorenie krivky grafu danej funkcie
        z = np.array([self.func([x, y]) for x, y in zip(np.ravel(x), np.ravel(y))])
        z = z.reshape(x.shape)

        # Zostavenie grafu pomocu suradnic
        self.ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap=plt.get_cmap('jet'), alpha=0.3)

        # Pomenovanie grafu a jednotlivých os
        self.ax.set_title(figName)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        # Cesta bodov v animacii
        self.path = []
        # Populacia, ktorá se bude animovat (historia priechodu)
        self.population_to_anim = population_history

        # Vykreslenie animací
        # => vykreslená historia priechodu je zobrazena červenou
        if self.population_to_anim != None:
            anim = matplb.animation.FuncAnimation(self.fig, self.animByPopulation, len(self.population_to_anim), interval=interval_anim, blit=False, repeat=False)

        # Vykreslenie najlepšieho jedinca získaného z vyhladávacieho algoritmu
        # => výsledný jedinec je vykresleny zelenou
        if best_individual != None:
            self.ax.scatter3D(best_individual.coordinates[0], best_individual.coordinates[1], best_individual.f, c = '#00ff00')

        plt.show()

    # Vykreslenie animacie
    def anim(self, n):
        # Pokial je už vykreslený predchádzajuci bod, tak ho odstraň
        if self.path != None:
            self.path.remove()

        # Ak existuje bod pre vykreslenie, tak ho vykresli
        if self.points_to_anim != None:
            self.path = self.ax.scatter3D(self.points_to_anim[n].x, self.points_to_anim[n].y, self.points_to_anim[n].z, c = '#ff0000')

    def animByPopulation(self, n):
        # Ak su uz vykreslene predchadzajuce body, tak ho odstraň
        if self.path:
            for i in range(len(self.path)):
                if self.path[i]:
                    self.path[i].remove()
            self.path.clear()

        # Ak existujíubody pre vykreslenie, tak ich vykresli
        if self.population_to_anim != None:
            for individual in self.population_to_anim[n].individuals:
                self.path.append(self.ax.scatter3D(individual.coordinates[0], individual.coordinates[1], individual.f, c = '#ff0000'))
            
         