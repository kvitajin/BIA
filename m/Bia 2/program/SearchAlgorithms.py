from Point import Point
from Graph import Graph
import random
import numpy as np
import string
import copy

class SearchAlgorithms:

    def __init__(self):
        # city_index zaručuje jedinečnost v názvu města
        self.city_index = 0

    # Generuje město s náhodnou pozicí skrze interval s náhodným jedinečným jménem
    def GenerateCity(self, lowerBound, upperBound):
        city = Point(random.uniform(lowerBound, upperBound), random.uniform(lowerBound, upperBound), string.ascii_letters[self.city_index])
        self.city_index += 1
        return city

    # Generování měst
    def GenerateCities(self, amount, interval):
        array = []

        for _ in range(amount):
            array.append(self.GenerateCity(interval.lowerBound, interval.upperBound))

        return array

    # Výpočet vzdálenosti mezi dvěma městy
    def CalculateDistance(self, city_from, city_to):
        return np.sqrt((city_from.x - city_to.x)**2 + (city_from.y - city_to.y)**2)

    # Vygenerování populace
    def GeneratePopulation(self, number, cities):
        array = []

        # Pridání "promíchaných" měst pro každého jedince
        for _ in range(number):
            array.append(random.sample(cities, len(cities)))

        return array

    # Výpočet vzdálenosti mezi jednotlivými městy pro konkrétního jedince
    def EvaluateIndividual(self, individual):
        individual_length = len(individual)
        evaluation = 0

        # Průchod všemi městy
        for i in range(individual_length):
            # Pokud se jedná o poslední město, vypočti poslední vzdálenost mezi posledním městem a prvním a přičti k celku
            if i == individual_length - 1:
                evaluation += self.CalculateDistance(individual[i], individual[0])
                continue
            # Vypočti vzdálenost mezi aktuálním a následujícím městem a přičti k celku
            evaluation += self.CalculateDistance(individual[i], individual[i + 1])

        return evaluation

    # Vytvoření nového jedince skrze dva rodiče
    def Crossover(self, population1, population2):
        # Zkopíruji si population1
        array = copy.deepcopy(population1)
        # Promíchám
        random.shuffle(array)
        # Vyberu 1/2
        array = array[:int(len(population1)/2)]
        
        # Vezmu první polovinu měst z prvního jedince a vložím do nového
        #for i in range(int(len(population1)/2)):
            #array.append(population1[i])
        #    if not array:
        #        array.append(random.choice(population1))
        #    else:
        #        array.append(random.choice([x for x in array if x != population1[i]]))

        #array = random.sample(population1, int(len(population1/2)))
        

        found = False

        # Postupně procházím druhého jedince a kontroluji, jestli nový jedinec již město neobsahuje, pokud ne, tak vložím
        for i in range(len(population2)):
            for population in array:
                if population2[i] is population:
                    found = True
                    break
            if found is False:
                array.append(population2[i])
            found = False
        
        return array

    # Mutace populace
    def Mutation(self, population):
        array = population
        # Uložím se idčka
        ids = range(len(array))
        # Vyberu si náhodně dva prvky
        i1, i2 = random.sample(ids, 2)
        # Vybrané dva prvky mezi sebou prohodím
        array[i1], array[i2] = array[i2], array[i1]

        return array

    # Samotný genetický algoritmus
    def GeneticAlgorithm(self, interval):
        NP = 20 # Počet jedinců
        G = 200 # Počet generací
        D = 20  # Počet měst
        # Vygenerování měst
        cities = self.GenerateCities(D, interval)
        # Vygenerování populace
        population = self.GeneratePopulation(NP, cities)

        # Historie pro vykreslení v animaci
        points_history = []
        the_best_found_in_population = None

        # Pseudokód využit z prezentace
        for i in range(G):
            # Vytvoření deepcopy jako záloha
            new_population = copy.deepcopy(population)
            # Průchod jedinců v populaci
            for j in range(NP):
                # Výběr aktuálního jedince
                parent_A = population[j]
                # Výběr náhodného jedince, který ale není aktuálním
                parent_B = random.choice([x for ii, x in enumerate(population) if ii != j])
                # Vytvoření nového potomka skrze crossover
                offspring_AB = self.Crossover(parent_A, parent_B)
                # 50% šance na mutaci
                if np.random.uniform() < 0.5:
                    # Zmutování potomka (prohození dvou měst)
                    offspring_AB = self.Mutation(offspring_AB)
                    
                evalAB = self.EvaluateIndividual(offspring_AB)
                evalA = self.EvaluateIndividual(parent_A)
                #print("evalAB ", evalAB, " | evalA", evalA)

                # Výpočet celkové vzdálenosti u potomka a rodiče A
                if  evalAB < evalA:
                    # Pokud má potomek celkovou vzdálenost menší, než rodič A, tak nahradí rodiče A
                    new_population[j] = offspring_AB


                if the_best_found_in_population is None:
                    the_best_found_in_population = new_population[j]
                elif self.EvaluateIndividual(the_best_found_in_population) > self.EvaluateIndividual(new_population[j]):
                    the_best_found_in_population = new_population[j]

                #print(self.EvaluateIndividual(new_population[j]))
                points_history.append(copy.deepcopy([the_best_found_in_population]))

            population = new_population
            #points_history.append(copy.deepcopy([the_best_found_in_population]))
            #points_history.append(copy.deepcopy(population))

        graph = Graph(interval)
        graph.Show("Genetic Algorithm", cities, points_history)
