import random
import numpy as np
from Individual import Individual
from operator import attrgetter

class Population:

    # Privátna premenna, ktorá naberá hodnoty true, ak už jedinci boli ohodnoteni (kvoli výbrru najlepšieho jedinca)
    __individualsWereCalculated = False
    # Privátna hodnota indexu prr následujúceho jedinca
    __lastCreatedIndex = 0

    def __init__(self, cities):
        self.individuals = []
        self.cities = cities

    # Navýšenie indexu pre nového jedinca
    def __IncrementLastCreatedIndex(self):
        self.__lastCreatedIndex += 1

    # Generuje jedinečného jedinca so startovacím mestom
    def GenerateIndividual(self, city):
        individual = Individual(city, len(self.cities.Return()), self.__lastCreatedIndex)
        self.__IncrementLastCreatedIndex()
        
        return individual

    # Vytvorenie populacie jedincov
    def GenerateIndividuals(self, number):
        if self.individuals:
            return

        for i in range(number):
            self.individuals.append(self.GenerateIndividual(self.cities.Return()[i]))

    # Pridanie nového mesta pre všetky jedincov
    def CalculateIndividuals(self):
        self.__individualsWereCalculated = True
        
        for i in range(len(self.individuals)):
            self.CalculateIndividual(i)

    # Pridanie nového mesta na základe výpočtu pravdepodobnosti
    def CalculateIndividual(self, individual_id):
        alpha = 1
        beta = 2

        probabilities = {}      # Pravdepodobnosti pre jednotlive vybrané mesta
        probability_sum = 0     # Suma sučtu vzdialeností mezi vybraným mestem a ostatními

        # Priechod všetkých miest
        for i in range(len(self.cities.Return())):
            # Ak vybrane mesto sa už nachádza v ceste u jedinca (jedinec už mesto navštívil), tak pokračuj k ďalšiemu
            if any(x.name == self.cities.Return()[i].name for x in self.individuals[individual_id].path):
                continue
            # Posledné navštívené mesto
            last_visited_city = self.individuals[individual_id].path[len(self.individuals[individual_id].path) - 1]
            # Výpočet hornej časti - pheromon[posledné navštívené mesto][aktuálne vybrane nenavštívené mesto]^aplha * visibility_matrix[poslední navštívené město][aktuálně vybrané nenavštívené město]^beta
            probability = self.cities.pheromones[last_visited_city.index][i]**alpha * self.cities.visibility_matrix[last_visited_city.index][i]**beta
            # Pridanie pravdepodobnosti pre konkrétne mesto (cestu k danému mestu)
            probabilities[i] = probability
            # Přičítanie hodnoty do sumy
            probability_sum += probability

        # Ak suma naberá hodnoty 0, tak je jasné, že sa nachádzame u priechodu posledné mesto - prvne mesto, kde nemusíme hodnotu počítat,
        # respektive trasa je už kompletná a je zbytočné pridávať opät prvé mesto, ktoré je už na prvej pozici
        if probability_sum == 0:
            return

        # Výber náhodnej hodnoty pre výber nového mesta do cesty
        r = random.uniform(0, 1)
        probability_percentage = 0
        result = None

        # Priechod hodnot pravdepodobností u jednotlivých tras
        for key in probabilities:
            # Přepočet pravdepodobnosti na základe sumy
            probabilities[key] = probabilities[key] / probability_sum
            # Přičítanie k percentualnej šanci
            probability_percentage += probabilities[key]
            # Výber následujuceho mesta na základe percentuálnej pravdepodobnosti
            # Ak bolo mesto vybrane, tak nema smysel pokračovat v cykle dalej
            if r <= probability_percentage:
                result = self.cities.Return()[key]
                break
        
        # Přidání nového mesta do cesty
        self.individuals[individual_id].path.append(result)

    # Prepočitanie feromonov na základe prichodov cest všetkých mravencov
    def RecalculatePheromones(self):
        Q = 1
        # Matice pre sučet jedtnolivých vzdialeností pre konkrétne mesta
        recalculation_matrix = np.zeros((len(self.cities.pheromones), len(self.cities.pheromones)))
        for individual in self.individuals:
            # Výpočet celkove vzdialenosti pre konkrétneho jedinca
            evaluation = individual.EvaluateDistance(self.cities.CalculateDistance)
            individual_length = len(individual.path)
            # Přičítanie hodnoty Q/f(s) pre všetky pozicie, ktoré konkrétne jedince navštívil
            for i in range(individual_length):
                # Ak sa nachádzame na hodnote posledneho mesta, tak prevedieme výpočet s posledným a prvím
                if i + 1 == individual_length:
                    recalculation_matrix[individual.path[individual_length - 1].index][individual.path[0].index] += Q / evaluation
                    break

                recalculation_matrix[individual.path[i].index][individual.path[i + 1].index] += Q / evaluation

        p = 0.5
        # Výsledný prepočet vaporizacie feromonov
        for i in range(len(self.cities.pheromones)):
            for j in range(len(self.cities.pheromones[i])):
                self.cities.pheromones[i][j] = (1 - p) * self.cities.pheromones[i][j] + recalculation_matrix[i][j]

    # Vyresetuje pozicie všetkých jedincov
    def ResetIndividuals(self):
        for i in range(len(self.individuals)):
            self.individuals[i].ResetPath()
        
    # Funkcie vracia najlepšieho jedinca, ak neboli ešte jedinci ohodnoteny, vráti sa hodnota None
    def GetBestIndividual(self):
        if not self.__individualsWereCalculated:
            return None
        return min(self.individuals, key = attrgetter("currentDistance"))
