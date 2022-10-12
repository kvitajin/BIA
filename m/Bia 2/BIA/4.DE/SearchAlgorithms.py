from Point import Point
from Graph import Graph
import random
import numpy as np
import copy

class SearchAlgorithms:

    # Generuje náhodné hodnoty pre vyhledávání skrz hodnoty z intervalu a dimenzie
    def GenerateArray(self, lowerBound, upperBound, dimension):
        array = []

        for _ in range(dimension):  
            array.append(random.uniform(lowerBound, upperBound))
            
        return array

    # Vytvorenie populace jedincov
    def GeneratePopulation(self, number, interval, dimension):
        array = []

        for _ in range(number):
            array.append(self.GenerateArray(interval.lowerBound, interval.upperBound, dimension))
        return array

    # Výpočet vektoru "v" pre smer nového bodu, samotná funkcia kontroluje hranice okraja funkcie
    def CalculateVector(self, x1, x2, x3, interval, dimension):
        F = 0.5
        v = []

        for i in range(dimension):
            result = (x1[i] - x2[i]) * F + x3[i]
            if result <= interval.lowerBound:
                result = interval.lowerBound
            elif result >= interval.upperBound:
                result = interval.upperBound
            v.append(result)

        return v

    # Samotný algoritmus diferenciálnej evolucie vytvorenie z pseudokódu z prezentacie
    def DifferentialEvolution(self, dimension, interval, func, figName, interval_anim = 1):
        NP = 4          # počet jedincov
        CR = 0.5        # crossover rozsah
        g_maxim = 10    # počet generačnych cyklov

        # Vytvorenie populacie jedincov
        pop = self.GeneratePopulation(NP, interval, dimension)
        g = 0

        # Body pre vykreslenie do animacie
        points_history = []
        best_point = None

        while g < g_maxim:
            new_pop = copy.deepcopy(pop)
            for i, x in enumerate(pop, start = 0):
                # Nájdenie náhodných troch jedincov kde r1 != r2 != r3 != x, kde x je aktuálně vybraný jedinec
                r1, r2, r3 = random.choice([(x, y, z) for num_x, x in enumerate(pop, start = 0) for num_y, y in enumerate(pop, start = 0) for num_z, z in enumerate(pop, start = 0) if num_x != num_z != num_y != i])
                # Výpočet vektorů
                v = self.CalculateVector(r1, r2, r3, interval, dimension)
                u = np.zeros(dimension)
                j_rnd = np.random.randint(0, dimension)

                # Vytvorenie crossoveru
                for j in range(dimension):
                    if np.random.uniform() < CR or j == j_rnd:
                        # Aspoň jedna hodnota by mala obsahovat mutačnú hodnotu "v" thx to konstante "F"
                        u[j] = v[j]
                    else:
                        u[j] = x[j]

                # Výpočet hodnôt na funkcii
                f_u = func(u)
                f_x_i = func(x)

                # Porovnanie hodnot funkcií, kde pokiaľ je f_x_i >= f_u, tak bola najdena lepšia hodnota a prijme se nový potomok
                if f_u <= f_x_i:
                    point = Point(u[0], u[1], f_u)
                    points_history.append(point)
                    new_pop[i][0] = u[0]
                    new_pop[i][1] = u[1]
                    if best_point is None:
                        best_point = point
                    elif f_u < best_point.z:
                        best_point = point
            g += 1
            pop = new_pop

        # Zostavenie grafu
        graph = Graph(func, interval)
        graph.Show(figName, [best_point], points_history, interval_anim)