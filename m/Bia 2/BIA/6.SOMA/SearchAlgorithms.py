from Point import Point
from Graph import Graph
from Population import Population
from Individual import Individual
import random
import numpy as np
import copy

class SearchAlgorithms:

    def SelfOrganizingMigration(self, dimension, interval, func, figName, interval_anim):
        pop_size = 30       # Velkost populacie
        PRT = 0.4           # Pravdepodobnost pre smer pohybu 0.1-0.4
        PathLength = 3.0    # Počet skokov na trase k leadrovi 
        Step = 0.11         # Vzdialenost skokov
        M_max = 10          # Počet migracií

        # Vytvorenie populacie jedincov
        population = Population(interval, dimension)
        population.GenerateIndividuals(pop_size)
        # Vypočítanie hodnot na funkcii pre všetkych jedincov
        population.CalculateIndividuals(func)
        # Nájdenie najlepšieho jedinca (leadera)
        individual_best = copy.deepcopy(population.GetBestIndividual())

        m = 0
        t = Step

        # Pole historie populacii pre vykreslenie do animacie
        population_history = []
        population_history.append(copy.deepcopy(population))

        # Priechod migraciami
        while m < M_max:
            # Priechod jedincov v populaci
            for individual in population.individuals:
                # Ak je aktuálne vybraný jedinec leader, prevede sa skip (leader se nepresuvá)
                if individual.index == individual_best.index:
                    continue
                
                # Priechod trasy k leadrovi "individual_best"
                while t <= PathLength:
                    # Vytvoření hodnoty PRTVector pre výpočet novej pozicie
                    PRTVector = 1 if random.uniform(0, 1) < PRT else 0
                    # Výpočet aktuálne nájdenej pozicie
                    current_position = individual.CalculateNewPosition(t, PRTVector, individual_best, interval)
                    # Cost value zistim
                    current_position_f = individual.CalculateNewPositionF(func, current_position)

                    # Kontrola aktuálne najdenej pozicie s zatial nejlepšou najdenou novou poziciou
                    if current_position_f <= individual.new_position_f:
                        individual.new_position_f = current_position_f
                        individual.new_position = current_position

                    t += Step
                # Uloží sa najlepšia nová pozicia ako aktuálna pozicia
                individual.SavePosition()
                t = Step
            # Najdenie noveho najlepšieho jedinca (leadra)
            individual_best = copy.deepcopy(population.GetBestIndividual())
            m += 1
            # Pridanie populacie do historie pre vykreslenie
            population_history.append(copy.deepcopy(population))
        
        # Vypiše najlepšiue najdene hodnoty a pozicie
        print("The best found value at", figName, "function is", round(individual_best.f, 4), "at [", round(individual_best.coordinates[0], 4), "|", round(individual_best.coordinates[1], 4), "]")

        # Zostavenie grafu
        graph = Graph(func, interval)
        graph.ShowByPopulation(figName, individual_best, population_history, interval_anim)

