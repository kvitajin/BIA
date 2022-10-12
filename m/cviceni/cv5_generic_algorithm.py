import numpy as np
 
from numpy import abs, cos, exp, mean, pi, prod, sin, sqrt, sum
import mpl_toolkits.mplot3d.axes3d as ax3
import matplotlib.animation as anim

import pandas as pd

import random, operator
from matplotlib import cm
import matplotlib.pyplot as plt

import math
from pprint import pprint

class City:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

    def distance(self, city):
        xDis = abs(self.x - city.x)
        yDis = abs(self.y - city.y)

        return np.sqrt((xDis ** 2) + (yDis ** 2))

    def __repr__(self):
        return "(" + self.name + " | X: " + str(self.x) + ", Y: " + str(self.y) + ")"

class Fitness:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness = 0.0

    def routeDistance(self):
        if self.distance == 0:
            pathDistance = 0
            for i in range(0, len(self.route)):
                fromCity = self.route[i]
                toCity = None

                if i + 1 < len(self.route):
                    toCity = self.route[i + 1]
                else:
                    toCity = self.route[0]
                pathDistance += fromCity.distance(toCity)
            self.distance = pathDistance
        return self.distance

    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
        return self.fitness

def createRoute(cityList):
    return random.sample(cityList, len(cityList))

def initialPopulation(popSize, cityList):
    population = []

    for i in range(0, popSize):
        population.append(createRoute(cityList))
    
    return population

def rankRoutes(population):
    fitnessResults = {}

    for i in range(0, len(population)):
        fitnessResults[i] = Fitness(population[i]).routeFitness()

    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

def selection(popRanked, eliteSize):
    selectionResults = []
    df = pd.DataFrame(np.array(popRanked), columns = ['Index', 'Fitness'])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100 * df.cum_sum / df.Fitness.sum()

    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])

    for i in range(0, len(popRanked) - eliteSize):
        pick = 100 * random.random()

        for i in range(0, len(popRanked)):
            if pick <= df.iat[i, 3]:
                selectionResults.append(popRanked[i][0])
                break

    return selectionResults

def matingPool(population, selectionResults):
    matingpool = []

    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])

    return matingpool

def breed(parent1, parent2):
    child = []
    childP1 = []
    childP2 = []

    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))

    startGene = min(geneA, geneB)   
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])

    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2

    return child

def breedPopulation(matingpool, eliteSize) -> list:
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0, eliteSize):
        children.append(matingpool[i])

    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool) - i - 1])
        children.append(child)

    return children


def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))

            city1 = individual[swapped]
            city2 = individual[swapWith]

            individual[swapped] = city2
            individual[swapWith] = city1

    return individual

def mutatePopulation(population, mutationRate) -> list:
    mutatedPop = []

    for i in range(0, len(population)):
        mutatedInd = mutate(population[i], mutationRate)
        mutatedPop.append(mutatedInd)
    
    return mutatedPop

def nextGeneration(currentGen, eliteSize, mutationRate) -> list:
    popRanked = rankRoutes(currentGen)
    selectionResults = selection(popRanked, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPopulation(matingpool, eliteSize)
    nextGeneration = mutatePopulation(children, mutationRate)
    
    return nextGeneration

def posToChar(pos):
    return chr(pos + 65)

def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations):
    pop = initialPopulation(popSize, population)

    bestOf = []
    distance = []
    lastdist = np.inf

    for i in range(0, generations):
        pop = nextGeneration(pop, eliteSize, mutationRate)
        ranked = rankRoutes(pop)[0]        
        if lastdist > (1 / ranked[1]):
            distance.append(1 / ranked[1])
            bestOf.append(pop[ranked[0]])
            print(1/ranked[1])
            lastdist = (1 / ranked[1])

    bestRouteIndex = rankRoutes(pop)[0][0]
    bestRoute = pop[bestRouteIndex]
    visualize(bestOf, distance)
    return bestRoute

def visualize(arr, distances):
    fig, ax = plt.subplots()

    index = 0
    for i in arr:
        ax.clear()

        for l in range(0, len(i)):
            ax.text(i[l].x * (1 + 0.02), i[l].y * (1 + 0.02) , i[l].name, fontsize=8)
            if l < len(i)-1:
                x = [i[l].x, i[l+1].x]
                y = [i[l].y, i[l+1].y]
                ax.plot(x, y, 'o-r', linewidth=2, markersize=6, markerfacecolor='blue', markeredgecolor='k')
            else:
                #Check ending
                x = [i[l].x, i[0].x]
                y = [i[l].y, i[0].y]
                ax.plot(x, y, 'o-r', linewidth=2, markersize=6, markerfacecolor='blue', markeredgecolor='k')

        ax.set_title("Distance: " + str(distances[index]))
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

        index += 1
        plt.pause(0.10)

    plt.show()



if __name__ == "__main__":
    cityList = []

    citySize = 15
    
    for i in range(0, citySize):
        cityList.append(City(x = random.randint(0, 200), y = random.randint(0, 200), name = posToChar(i)))

    r = geneticAlgorithm(
        population = cityList, 
        popSize = len(cityList), 
        eliteSize = round(len(cityList)/10),
        mutationRate = 0.01,
        generations = 500
    )