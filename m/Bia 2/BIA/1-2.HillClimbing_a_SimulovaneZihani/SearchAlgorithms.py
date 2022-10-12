from Point import Point
from Graph import Graph
import random
import numpy as np

class SearchAlgorithms:

    # Generuje náhodné hodnoty pre vyhľadávánie skrz hodnoty z intervalu a dimenzie
    def GenerateArray(self, lowerBound, upperBound, dimension):
        array = []
        for _ in range(dimension):  
            array.append(random.uniform(lowerBound, upperBound))
            
        return array

    # Spraví kontrolu nového bodu a jeho pohybu na konkrétnomm intervalu
    def CalculatePoint(self, coordinates, coordinates_of_movement, interval):
        coordinates_of_movement[0] = coordinates[0] if coordinates_of_movement[0] + coordinates[0] <= interval.lowerBound or coordinates_of_movement[0] + coordinates[0] >= interval.upperBound else coordinates_of_movement[0] + coordinates[0]
        coordinates_of_movement[1] = coordinates[1] if coordinates_of_movement[1] + coordinates[1] <= interval.lowerBound or coordinates_of_movement[1] + coordinates[1] >= interval.upperBound else coordinates_of_movement[1] + coordinates[1]
        
        return coordinates_of_movement

    def HillClimbing(self, cycles, dimension, interval, func, figName, interval_anim = 1):
        # Výber prvého náhodného bodu
        random_choice = self.GenerateArray(interval.lowerBound, interval.upperBound, dimension)
        best_choice = func(random_choice)
        # Výsledný bod / body
        points = []
        # Historia postupu bodov
        points_history = []
        i = 1
        # Počet bodov pre jeden cyklus (koľko bodov sa má rozhádzať v rozmedzí intervalu)
        test_range = 10
        # Rozsah bodov, v kterom sa môžu pohybovať v danom cykle
        test_interval = [-interval.step, interval.step]
        temporary_result = random_choice
        while i <= cycles:
            for _ in range(test_range):
                # Vygenerovanie bodu (mutácia) v okolí test_invervalu
                random_mutation = self.GenerateArray(test_interval[0], test_interval[1], dimension)
                # Přiradenie bodu do funkce
                random_mutation = self.CalculatePoint(random_choice, random_mutation, interval)
                mutation_result = func(random_mutation)

                # Kontrola, či je zmutovaný bod lepší, než aktuálna najlepšia hodnota
                if mutation_result <= best_choice:
                    temporary_result = random_mutation
                    best_choice = mutation_result

            # Uloženie aktuálneho najlepšieho výsledku v danom cykle
            random_choice = temporary_result
            i += 1
            # Priradenie aktuálne nejlepšieho výsledku do historie
            point = Point(random_choice[0], random_choice[1], best_choice)
            points_history.append(point)

        # Priradenie najlepšieho nájdeného bodu do výsledku pre vykreslenie
        point = Point(random_choice[0], random_choice[1], best_choice)
        points.append(point)

        # Zostavenie grafu
        graph = Graph(func, interval)
        graph.Show(figName, points, points_history, interval_anim)

        return best_choice, random_choice

    def SimulatedAnnealing(self, cycles, dimension, interval, func, figName, interval_anim = 1):
        # Aktuálna teplota
        T_0 = 100
        # Minimálna teplota
        T_min = 0.5
        # Tempo chladenie
        alpha = 0.95

        T = T_0

        # Vygenerovanie prvého náhodného bodu
        x_a = self.GenerateArray(interval.lowerBound, interval.upperBound, dimension)
        x = func(x_a)
        
        # Interval testovania v okolí okolo bodu
        test_interval = [-interval.step, interval.step]

        # Body pre vykreslenie
        points_history = []
        points = []

        # Náhodné hodnoty výsledku
        best_result = 8000
        best_result_coordinates = [800,800]

        while T > T_min:
            for _ in range(cycles):
                # Vygenerovanie bodu (mutace) v okolí test_invervalu
                x_1_a = self.GenerateArray(test_interval[0], test_interval[1], dimension)
                
                # Priradenie bodu do funkcie
                x_1_a = self.CalculatePoint(x_a, x_1_a, interval)
                x_1 = func(x_1_a)

                # Kontrola nájdeného bodu, ak je menšia než aktuálny výsledok, tak sa prepíše (hladá se minimum)
                if x_1 < x:
                    x = x_1
                    x_a = x_1_a
                    point = Point(x_a[0], x_a[1], x)
                    points_history.append(point)

                    # Ak je aktuálny bod lepší, než celkovo nejlepší nájdený bod, tak sa prepíše ako hlavný výsledok
                    if x < best_result:
                        best_result = x
                        best_result_coordinates = x_1_a
                # Prehľadávánie okolia
                else:
                    r = random.uniform(0, 1)

                    if r < np.e**(-(x_1 - x) / T):
                        x = x_1
                        x_a = x_1_a
                        point = Point(x_a[0], x_a[1], x)
                        points_history.append(point)
            # Zníženie teploty
            T = T * alpha

        # Priradenie najlepšieho nájdeného bodu do výsledku pre vykreslenie
        point = Point(best_result_coordinates[0], best_result_coordinates[1], best_result)
        points.append(point)

        # Zostavenie grafu
        graph = Graph(func, interval)
        graph.Show(figName, points, points_history, interval_anim)

        return best_result, best_result_coordinates