from Cities import Cities
from Population import Population
from Graph import Graph
import random
import numpy as np
import string
import copy

class SearchAlgorithms:

    # Samotný genetický algoritmus
    def AntColony(self, interval):
        M = 50 # Počet priebehov
        N = 20  # Počet mest a jedincov
        # Vygenerovanie mest
        cities = Cities(interval)
        cities.Generate(N)
        # Vygenerovanie populacie
        population = Population(cities)
        population.GenerateIndividuals(N)

        # Historia pre vykreslenie v animacii
        points_history = []

        best_result = None

        # Priechod cyklov priebehu, kde mravci hladajú najlepšiu cestu
        for i in range(M):
            # Priechod počtu mest, kde každým jedným priechodom je pridane jedno nové mesto pre každého jedinca
            for j in range(N):
                # Každý mravec si na základe pravdepodobnosti skrz feromony pridá jedno následujuce mesto
                population.CalculateIndividuals()
            # Po skončení cyklu už každý mravec pozná celu svoju cestu
            # Preto je nezbytné na zaklade ich cest prepočítať feromoný
            population.RecalculatePheromones()
            
            # Prevedie sa výber najelpšieho jedinca na základr dlzky jeho cesty
            result = copy.deepcopy(population.GetBestIndividual())
            # Ak ešte nemáme žiadny výsledok, ptm sa nastaví ako najlepší
            if best_result is None:
                best_result = result
            # Ak už výsledok máme, tak ho porovnáme s aktuálnym, ak je aktuálny lepší (menší), ptm se prevedie prepis
            elif result.currentDistance < best_result.currentDistance:
                best_result = result
            # Najlepší najdený výsledok sa uloží do historie priechodov
            points_history.append([best_result])
            # Nakoniec sa prevedie reset cesty všetkým jedincom pre vytvorenie nového priechodu na základe feromonov
            population.ResetIndividuals()

        # Zobrazenie grafu
        graph = Graph(interval)
        graph.Show("Ant Colony Optimization", cities.Return(), points_history)
