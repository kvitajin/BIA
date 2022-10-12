import numpy as np

import mpl_toolkits.mplot3d.axes3d as ax3
import matplotlib.animation as anim

import copy

import random, operator
from matplotlib import cm
import matplotlib.pyplot as plt

import math
from pprint import pprint

def sphere(*params):
    sum1 = []

    for i in range(len(params)):
        sum1.append(params[i]**2)

    return sum(sum1)

def schwefel(*params):
    sum1 = []

    for i in params:
        sum1.append(i*np.sin(np.sqrt(np.abs(i))))

    z = 418.9829 * len(params) - sum(sum1)

    return z

def rosenbrock(*params):
    sum1 = []

    for i in range(0, len(params)-1):
        sum1.append(100*(params[i+1] - params[i]**2)**2 + (params[i] - 1)**2)
        
    return sum(sum1)

def rastrigin(*params):
    sum1 = []

    for i in params:
        sum1.append(i**2 - 10*np.cos(2*np.pi*i))

    z = 10*len(params) + sum(sum1)

    return z

def griewank(*params):
    sum1 = []
    prod1 = []
    i = 1

    for val in params:
        sum1.append((val**2)/4000)
        prod1.append(np.cos(val / (np.sqrt(i))) + 1)
        i = i + 1

    z = sum(sum1) - np.product(prod1)
    return z

def levy(*params):
    sum1 = []
    w_d = 1 + ((params[len(params)-1] - 1) / 4)
    w_1 = 1 + ((params[0] - 1) / 4)

    for i in range(0, len(params)-1):
        w_i = 1 + ((params[i] - 1) / 4)
        sum1.append( (w_i - 1)**2 * (1 + 10*np.sin(np.pi*w_i+1)**2) + (w_d-1)**2 * (1+np.sin(2*np.pi*w_d)**2) )

    z = np.sin(np.pi*w_1)**2 + sum(sum1)
    return z

def michalewicz(*params):
    sum1 = []
    m = 10
    i = 1

    for val in params:
        sum1.append(np.sin(val) * np.sin((i*val**2)/np.pi)**(2*m))
        i = i + 1

    return -1*sum(sum1)

def zakharov(*params):
    sum1 = []
    sum2 = []
    sum3 = []

    i = 1
    for x in params:
        sum1.append(x**2)
        sum2.append(0.5*i*x)
        sum3.append(0.5*i*x)
        i = i + 1

    z = sum(sum1) + (sum(sum2))**2 + (sum(sum3))**4
    return z

def ackley(*params):
    a = 20
    b = 0.2
    c = 2 * np.pi
    sum1 = []
    sum2 = []

    for i in params:
        sum1.append(i**2)
        sum2.append(np.cos(c*i))

    part1 = -a * np.exp(-b*np.sqrt(sum(sum1)/len(params)))
    part2 = -np.exp(sum(sum2)/len(params))

    return a + np.exp(1) + part1 + part2


class Firefly():
    def __init__(self, fnc, lb, ub, dimens):
        #Generate random position clipped to bounds and set default vars
        normalized = np.random.rand(dimens)

        #Denormalize the value according to lb/ub
        diff = np.fabs(lb - ub)
        self.func = fnc
        self.position = lb + normalized * diff
        self.light = self.func(*self.position)

        #self.update_light()

    def update_light(self, r, gamma):
        l0 = self.func(*self.position)
        self.light = l0 * np.e**( -gamma * r)

class Optimizer():
    def __init__(self, pop_size, dimens, lb, ub, generations, gamma, alpha, beta_init, beta_min, fnc):
        self.pop_size = pop_size
        self.dimens = dimens
        self.lb = lb
        self.ub = ub
        self.generations = generations
        self.gamma = gamma
        self.alpha = alpha
        self.beta_init = beta_init
        self.beta_min = beta_min
        self.func = fnc

        #Generate initial population
        self.population = [Firefly(self.func, self.lb, self.ub, self.dimens) for i in range(self.pop_size)]
        self.solutions = []

    def step(self):
        tmp_pop = copy.deepcopy(self.population)

        for i in range(self.pop_size):
            for j in range(self.pop_size):
                #Skip itself and the best one (the best is always on the top)
                if i == j or i == 0:
                    continue

                r = np.sqrt(np.sum((self.population[i].position - tmp_pop[j].position) ** 2))

                self.population[i].update_light(r, self.gamma)
                self.population[j].update_light(r, self.gamma)

                if self.population[j].light < tmp_pop[i].light:
                    #beta = (self.beta_init - self.beta_min) * math.exp(-self.gamma * r ** 2) + self.beta_min
                    beta = self.beta_init / (1 + r)

                    for k in range(self.dimens):
                        normal = np.random.normal(0, 1)
                        self.population[i].position[k] += beta * (tmp_pop[j].position[k] - self.population[i].position[k]) + self.alpha * normal 
                        #BOUNDARIES CHECK
                        self.population[j].position[k] = np.clip(self.population[j].position[k], self.lb, self.ub)
        
        self.population.sort(key = operator.attrgetter('light'), reverse = True)

        best_copy = copy.deepcopy(self.population[0])
        normal = np.random.normal(0, 1)

        for i in range(self.dimens):
            best_copy.position[i] += self.alpha * normal

        if self.func(*self.population[0].position) > self.func(*best_copy.position):
            self.population[0] = best_copy

        self.solutions.append(copy.deepcopy(self.population))

    def visualize(self):
        fig = plt.figure()
        ax = fig.gca(projection='3d')

        X = np.linspace(self.lb, self.ub, 200)
        Y = np.linspace(self.lb, self.ub, 200)
        X, Y = np.meshgrid(X, Y)
        Z = self.func(X, Y)

        #Doing animation
        for i in range(self.generations):
            ax.clear()

            ax.plot_surface(X, Y, Z, alpha=0.6, cmap=cm.OrRd, linewidth=0.1, antialiased=True)
            ax.set_xlim([self.lb, self.ub])
            ax.set_ylim([self.lb, self.ub])

            first = True
            for j in self.solutions[i]:
                if first:
                    #Marking the best one (first)
                    ax.plot(j.position[0], j.position[1], self.func(j.position[0], j.position[1]), 'go')
                else:
                    ax.plot(j.position[0], j.position[1], self.func(j.position[0], j.position[1]), 'ro')
                first = False

            plt.pause(0.05)
        
        plt.show()

    def run(self):
        for i in range(self.generations):
            self.step()

        self.visualize()


if __name__ == "__main__":
    #Parameters
    p_pop_size = 10
    p_dimens = 2
    p_lb = -6
    p_ub = 6
    p_generations = 200
    p_gamma = 0.97
    p_alpha = 0.3
    p_beta_init = 1
    p_beta_min = 0.2
    p_func = sphere

    firefly = Optimizer(p_pop_size, p_dimens, p_lb, p_ub, p_generations, p_gamma, p_alpha, p_beta_init, p_beta_min, p_func)
    firefly.run()
