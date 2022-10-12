import numpy as np

import mpl_toolkits.mplot3d.axes3d as ax3
import matplotlib.animation as anim

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
        self.best_position = self.position
        self.best_value = np.Inf
        self.velocity = np.zeros(dimens)

    def move(self):
        #Calculate new position according to velocity vector
        self.position = self.position + self.velocity

class Space():
    def __init__(self, func, lb, ub, dimens, m_max, c1, c2):
        #Set default vars
        self.particles = []
        self.lb = lb
        self.ub = ub
        self.dimens = dimens
        self.m = 0
        self.m_max = m_max
        self.w = 0
        self.c1 = c1
        self.c2 = c2
        self.func = func

        #Generate random global best
        normalized = np.random.rand(dimens)
        diff = np.fabs(lb - ub)
        self.gbest_position = lb + normalized * diff
        self.gbest_value = np.Inf
        self.gbest_list = []

    def generate_particles(self, n):
        #Generate initial population
        self.particles = [Particle(self.lb, self.ub, self.dimens) for _ in range(n)]

    def fitness(self, particle):
        #Calculate fitness of particle using Space's given function
        return self.func(*particle.position)

    def calculate_pgbest(self):
        gb_list = []

        for p in self.particles:
            f = self.fitness(p)
            if p.best_value > f:
            #Set new best pos and val
                p.best_value = f
                p.best_position = p.position
                #Add coords to list for visualization
                gb_list.append(p.best_position)

            if self.gbest_value > self.fitness(p):
                self.gbest_value = f
                self.gbest_position = p.position

        self.gbest_list.append(gb_list)


    def calculate_w(self, ws, we):
        #Calculate new inertia weight
        self.m = self.m + 1
        self.w = ws * ((ws - we) * self.m) / self.m_max

    def move_particles(self):
        for p in self.particles:
            #Calculate new velocity vector
            v = (self.w * p.velocity) + (self.c1 * random.random()) * (p.best_position - p.position) + (self.c2 * random.random()) * (self.gbest_position - p.position)

            p.velocity = v
            p.move()

    def visualize(self):
        fig = plt.figure()
        ax = fig.subplots()
        X = np.linspace(self.lb, self.ub, 200)
        Y = np.linspace(self.lb, self.ub, 200)
        X, Y = np.meshgrid(X, Y)
        Z = self.func(X, Y)

        for i in self.gbest_list:
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
    p_pop_size = 15
    p_dimens = 2
    p_m_max = 50
    p_c1 = 4.0
    p_c2 = 2.0
    p_ws = 0.9
    p_we = 0.4

    space = Space(p_func, p_lb, p_ub, p_dimens, p_m_max, p_c1, p_c2)
    space.generate_particles(p_pop_size)

    #Main loop
    for i in range(p_m_max):
        space.calculate_pgbest()
        space.calculate_w(p_ws, p_we)
        space.move_particles()

    space.visualize()
