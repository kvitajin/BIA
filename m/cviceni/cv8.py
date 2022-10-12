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

class Particle():
    def __init__(self, lb, ub, dimens):
        #Generate random position clipped to bounds and set default vars
        normalized = np.random.rand(dimens)

        #Denormalize the value according to lb/ub
        diff = np.fabs(lb - ub)
        self.position = lb + normalized * diff

class Space():
    def __init__(self, func, lb, ub, dimens, m_max, path_length, step, prt):
        #Set default vars
        self.particles = None
        self.lb = lb
        self.ub = ub
        self.dimens = dimens
        self.m = 0
        self.m_max = m_max
        self.w = 0
        self.path_length = path_length
        self.step = step
        self.prt = prt
        self.func = func
        
        self.visualization_list = []

    def generate_particles(self, n):
        #Generate initial population
        self.particles = [Particle(self.lb, self.ub, self.dimens) for _ in range(n)]

    def fitness(self, particle):
        #Calculate fitness of particle using Space's given function
        return self.func(*particle.position)

    def soma(self):
        iteration_best = self.get_best()

        for idx, p in enumerate(self.particles):
            t = 0
            old_one = copy.deepcopy(p)
            new_one = copy.deepcopy(p)
            p_one = copy.deepcopy(p)

            while t <= self.path_length:
                for i in range(self.dimens):
                    rnd = np.random.uniform(0, 1)
                    prt_vec = 0
                    if rnd < self.prt:
                        prt_vec = 1
                    
                    new_one.position[i] = np.add(old_one.position[i], np.multiply(np.subtract(iteration_best.position[i], old_one.position[i]), t * prt_vec))
                
                #CHECK BOUNDARIES
                new_one.position = np.clip(self.lb, self.ub, new_one.position)

                if self.fitness(new_one) < self.fitness(p_one):
                    p_one = copy.deepcopy(new_one)

                t = t + self.step

            if self.fitness(p_one) < self.fitness(old_one):
                self.particles[idx] = copy.deepcopy(p_one)

        #Visualization
        result_particles = []
        for i in self.particles:
            result_particles.append(i.position)

        self.visualization_list.append(result_particles)

    def get_best(self):
        p_val = self.fitness(self.particles[0])
        p = self.particles[0]

        for i in self.particles:
            new_val = self.fitness(i)
            if new_val < p_val:
                p_val = new_val
                p = i

        return p

    def visualize(self):
        fig = plt.figure()
        ax = fig.subplots()
        X = np.linspace(self.lb, self.ub, 200)
        Y = np.linspace(self.lb, self.ub, 200)
        X, Y = np.meshgrid(X, Y)
        Z = self.func(X, Y)

        for i in self.visualization_list:
            ax.clear()

            ax.pcolormesh(X, Y, Z.reshape(X.shape), shading='gouraud', cmap=cm.plasma)
            ax.set_xlim([self.lb, self.ub])
            ax.set_ylim([self.lb, self.ub])

            for j in i:
                ax.plot(j[0], j[1], 'ko')

            plt.pause(0.05)
        
        plt.show()

if __name__ == "__main__":
    #Parameters
    p_func = sphere
    p_lb = -20
    p_ub = 20
    p_path_length = 3.0
    p_step = 0.11
    p_pop_size = 20
    p_prt = 0.4
    p_dimens = 2
    p_m_max = 100

    space = Space(p_func, p_lb, p_ub, p_dimens, p_m_max, p_path_length, p_step, p_prt)
    space.generate_particles(p_pop_size)

    #Main loop
    for i in range(p_m_max):
        space.soma()

    space.visualize()
