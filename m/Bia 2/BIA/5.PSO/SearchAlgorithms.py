from Point import Point
from Graph import Graph
from Population import Population
from Individual import Individual
import random
import numpy as np
import copy

class SearchAlgorithms:

    # Algoritmus Particle Swarm zostavený podla kódu z prezentacie
    def ParticleSwarm(self, dimension, interval, func, figName, interval_anim):
        pop_size = 20   # Velkost populacie
        c_1 = 2.0       # Konstanta pre výpočet vektoru v
        c_2 = 2.0       # Konstanta pre výpočet vektoru v
        M_max = 100      # Počet generací

        velocity = [-interval.step*2, interval.step*2] # Aktuálne možná rychlost

        # Vytvorenie populace jedincov
        swarm = Population(interval, dimension)
        swarm.GenerateIndividuals(pop_size)
        # Vypočítanie hodnot na funkcii pre všetkych jedincov
        swarm.CalculateIndividuals(func)
        # Najdenie nejlepšieho jedinca
        gBest = copy.deepcopy(swarm.GetBestIndividual())
        # Pre každého jedinca se vypočítá vektor v
        swarm.CalculateVectorOfIndividuals(c_1, c_2, gBest, velocity)
        m = 0

        # Pole historie populací pre vykreslenie do animacie
        population_history = []
        population_history.append(copy.deepcopy(swarm))

        # Cyklus priechodov generací
        while m < M_max :
            # Cyklus prichodov jednotlivých jedincov
            for i, x in enumerate(swarm.individuals): 
                # Výpočet vektoru v na základe rychlosti velocity
                swarm.CalculateVectorOfIndividual(x, c_1, c_2, gBest, velocity)
                # Výpočet novej pozicie a prepísanie starej
                swarm.CalculateNewPosition(x)
                swarm.CalculateIndividual(func, x)
                
                # Kontrola hodnot na funkcií, kde x.f je aktuálna hodnota a x.pBestf aktuálne najlepsia  najdena pre konkrétneho jedinca
                if x.f < x.pBestf:
                    # Ak je x.f menšia, tak sme našli lepšiu hodnotu (minimum) a dojde k prepísániu aktuálne najlepšej hodnoty pre daného jedinca                
                    x.pBestf = x.f
                    for j in range(len(x.coordinates)):
                        x.pBest[j] = copy.deepcopy(x.coordinates[j])
                    
                    # Ak je najlepšia hodnota konkrétneho jedinca lepšia, tak u globálne najlepšieho jedinca, tak sa globánlny nahradí za aktuálneho
                    if x.pBestf < gBest.pBestf:
                        gBest = copy.deepcopy(x)

                #  výstupy pre kontrolu hodnôt
                #print(i, ". f: ", x.f, " x: ", x.coordinates[0], " y: ", x.coordinates[1])
                #print(i, ". pBestf: ", x.pBestf, " pBestX: ", x.pBest[0], " pBestY: ", x.pBest[1])
            m += 1
            # Pridanie populace do historie pre vykreslenie
            population_history.append(copy.deepcopy(swarm))

        # Zostavenie grafu
        graph = Graph(func, interval)
        graph.ShowByPopulation(figName, gBest, population_history, interval_anim)
