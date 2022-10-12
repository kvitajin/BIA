import random
import numpy as np
from Individual import Individual
from operator import attrgetter

class Population:

    # Privátna premmenná, ktorá naberá hodnoty true, pokiaľ už jedinci boli ohodnotený (kvôli výberu najlepšieho jedinca)
    __individualsWereCalculated = False

    def __init__(self, interval, dimension):
        self.interval = interval
        self.dimension = dimension
        self.individuals = []

    # Generuje náhodné hodnoty pre vyhladávánie skrz hodnoty z intervalu a dimenzie
    def GenerateIndividual(self):
        array = []

        for _ in range(self.dimension):  
            array.append(random.uniform(self.interval.lowerBound, self.interval.upperBound))
            
        individual = Individual(array)
        
        return individual

    # Vytvorenie populacie jedincov
    def GenerateIndividuals(self, number):
        if self.individuals:
            return

        for _ in range(number):
            self.individuals.append(self.GenerateIndividual())

    # Výpočet hodnôt na funkcii pre všetkych jedincov
    def CalculateIndividuals(self, func):
        self.__individualsWereCalculated = True

        for individual in self.individuals:
            individual.CalculateF(func)
            individual.GeneratepBest()

    # Výpočet hodnoty funkcie na konkrétnom jedincom
    def CalculateIndividual(self, func, individual):
        individual.CalculateF(func)

    # Výpočet nového vektoru na všetkých jedincov
    def CalculateVectorOfIndividuals(self, c_1, c_2, gBest, velocity):
        for individual in self.individuals:
            self.CalculateVectorOfIndividual(individual, c_1, c_2, gBest, velocity)

    # Výpočet nového vektoru na konkrétnom jedincovi
    def CalculateVectorOfIndividual(self, individual, c_1, c_2, gBest, velocity):
        r_1 = random.uniform(0, 1)
        r_2 = random.uniform(0, 1)
        individual.CalculateV(c_1, c_2, r_1, r_2, gBest, velocity, self.interval)

    # Výpočet novej pozicie pre daného jedinca, je tu obsiahnuta aj kontrola hranice intervalu funkcie
    def CalculateNewPosition(self, individual):
        length = len(individual.coordinates)

        for i in range(length):
            individual.coordinates[i] = individual.coordinates[i] + individual.v[i]
            if individual.coordinates[i] <= self.interval.lowerBound:
                individual.coordinates[i] = self.interval.lowerBound
            elif individual.coordinates[i] >= self.interval.upperBound:
                individual.coordinates[i] = self.interval.upperBound

    # Funkcie vracia najlepšieho jedinca, pokiaľ neboli eště jedinci ohodnotený, vrátí sa hodnota None
    def GetBestIndividual(self):
        if not self.__individualsWereCalculated:
            return None
        return min(self.individuals, key = attrgetter("f"))