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

class Graph:
    def __init__(self, matrix, rank):
        self.matrix = matrix
        self.rank = rank
        self.pheromone =[[1 / (rank * rank) for j in range(rank)] for i in range(rank)]

class Ant:
    def  __init__(self, aco, graph):
        self.aco = aco
        self.graph = graph
        self.total_cost = 0
        
        self.eta = [[0 if i == j else 1 / graph.matrix[i][j] for j in range(graph.rank)] for i in range(graph.rank)]

        self.allowed = [i for i in range(graph.rank)]
        self.not_allowed = []

        self.pheromone_delta = []

        start_node = random.randint(0, graph.rank - 1)
        self.not_allowed.append(start_node)

        self.allowed.remove(start_node)
        self.current_node = start_node

    def updatePheromoneDelta(self):
        self.pheromone_delta = np.zeros((self.graph.rank, self.graph.rank))

        for i in range(1, len(self.not_allowed)):
            j = self.not_allowed[i - 1]
            k = self.not_allowed[i]

            self.pheromone_delta[j][k] = self.aco.q / self.graph.matrix[j][k]

    def selectNext(self):
        bottom_part = 0
        for i in self.allowed:
            bottom_part += self.graph.pheromone[self.current_node][i] ** self.aco.alpha * self.eta[self.current_node][i] ** self.aco.beta

        probabilities = np.zeros(self.graph.rank)
        
        for i in range(self.graph.rank):
            try:
                self.allowed.index(i)
                probabilities[i] = self.graph.pheromone[self.current_node][i] ** self.aco.alpha * self.eta[self.current_node][i] ** self.aco.beta / bottom_part
            except:
                pass

        selected = 0
        rand = random.random()
        for i, probability in enumerate(probabilities):
            rand -= probability
            if rand <= 0:
                selected = i
                break

        self.allowed.remove(selected)
        self.not_allowed.append(selected)
        self.total_cost += self.graph.matrix[self.current_node][selected]
        self.current_node = selected

class Aco:
    def __init__(self, ants, gens, alpha, beta, rho, q):
        self.ants_count = ants
        self.gens = gens
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q

    def updatePheromones(self, graph, ants):
        for i, x in enumerate(graph.pheromone):
            for j, y in enumerate(x):
                graph.pheromone[i][j] *= self.rho

                for k in ants:
                    graph.pheromone[i][j] += k.pheromone_delta[i][j]

    def go(self, graph):
        best_cost = np.Inf
        best_costs = []
        best_solutions = []

        for g in range(self.gens):
            ants = [Ant(self, graph) for i in range(self.ants_count)]

            for a in ants:
                for i in range(graph.rank - 1):
                    a.selectNext()
                a.total_cost += graph.matrix[a.not_allowed[-1]][a.not_allowed[0]]

                #For visualize
                if a.total_cost < best_cost:
                    best_cost = a.total_cost
                    best_costs.append(best_cost)
                    best_solutions.append(a.not_allowed)

                a.updatePheromoneDelta()
            
            self.updatePheromones(graph, ants)

        return best_cost, best_costs, best_solutions

def posToChar(pos):
    return chr(pos + 65)

def visualize(costs, solutions, c):
    fig, ax = plt.subplots()

    for idx, i in enumerate(solutions):
        ax.clear()

        for idxx, l in enumerate(i):
            ax.text(c[l].x * (1 + 0.02), c[l].y * (1 + 0.02) , c[l].name, fontsize=8)
            if idxx < len(i)-1:
                x = [c[l].x, c[i[idxx+1]].x]
                y = [c[l].y, c[i[idxx+1]].y]
                ax.plot(x, y, 'o-r', linewidth=2, markersize=6, markerfacecolor='blue', markeredgecolor='k')
            else:
                #Check ending
                x = [c[l].x, c[i[0]].x]
                y = [c[l].y, c[i[0]].y]
                ax.plot(x, y, 'o-r', linewidth=2, markersize=6, markerfacecolor='blue', markeredgecolor='k')

        ax.set_title("Distance: " + str(costs[idx]))
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

        plt.pause(0.33)

    plt.show()



if __name__ == "__main__":
    p_city_count = 20
    p_ants_count = 20
    p_gens_count = 50
    p_alpha = 1.0
    p_beta = 5.0
    p_rho = 0.5
    p_q = 1
    p_lb = 0
    p_ub = 200

    cityList = [City(x = random.randint(p_lb, p_ub), y = random.randint(p_lb, p_ub), name = posToChar(i)) for i in range(p_city_count)]

    cost_matrix = []
    rank = len(cityList)

    for c in cityList:
        row = []

        for cc in cityList:
            row.append(c.distance(cc))
        cost_matrix.append(row)

    aco = Aco(p_ants_count, p_gens_count, p_alpha, p_beta, p_rho, p_q)
    graph = Graph(cost_matrix, rank)

    bcost, bcosts, bsolutions = aco.go(graph)

    #print('Best cost: {}, Best path: {}'.format(bcost, bsolutions[-1]))

    visualize(bcosts, bsolutions, cityList)
