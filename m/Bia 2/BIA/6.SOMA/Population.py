import random
import numpy as np
from Individual import Individual
from operator import attrgetter

class Population:

    # Privatna premmenná, ktorá naberá hodnoty true, ak už jedinci boli ohodnotený (kvoli výberu najlepšieho jedinca)
    __individualsWereCalculated = False
    # Privátna hodnota indexu pre následujuceho jedinca
    __lastCreatedIndex = 0

    def __init__(self, interval, dimension):
        self.interval = interval
        self.dimension = dimension
        self.individuals = []

    # Navýšenie indexu pre nového jedinca
    def __IncrementLastCreatedIndex(self):
        self.__lastCreatedIndex += 1

    # Generuje náhodné hodnoty pre vyhledávánie skrz hodnoty z intervalu a dimenzie
    def GenerateIndividual(self):
        array = []

        for _ in range(self.dimension):  
            array.append(random.uniform(self.interval.lowerBound, self.interval.upperBound))
            
        individual = Individual(array, self.__lastCreatedIndex)
        self.__IncrementLastCreatedIndex()
        
        return individual

    # Vytvorenie populacie jedincov
    def GenerateIndividuals(self, number):
        if self.individuals:
            return

        for _ in range(number):
            self.individuals.append(self.GenerateIndividual())

    # Výpočet hodnot na funkcii pre všetkych jedincov
    def CalculateIndividuals(self, func):
        self.__individualsWereCalculated = True

        for individual in self.individuals:
            individual.CalculateF(func)
            individual.GenerateNewPosition()

    # Výpočet hodnot funkcie na konkrétnom jedincovi
    def CalculateIndividual(self, func, individual):
        individual.CalculateF(func)

    # Funkcie vracia najlepšieho jedinca, pokil neboli ešte jedinci ohodnoteny, vrátí sa hodnota None
    def GetBestIndividual(self):
        if not self.__individualsWereCalculated:
            return None
        return min(self.individuals, key = attrgetter("f"))