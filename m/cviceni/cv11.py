import numpy as np

import mpl_toolkits.mplot3d.axes3d as ax3
import matplotlib.animation as anim

import copy

import random, operator
from matplotlib import cm
import matplotlib.pyplot as plt

import math
from pprint import pprint

from operator import attrgetter

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

def updatePoints(n, x, y, z, point):
    point.set_data(np.array([x[n], y[n]]))
    point.set_3d_properties(z[n], 'z')

    return point

class Student():
    def __init__(self, fnc, lb, ub, dimens):
        #Generate random position clipped to bounds and set default vars
        normalized = np.random.rand(dimens)

        #Denormalize the value according to lb/ub
        diff = np.fabs(lb - ub)
        self.func = fnc
        self.position = lb + normalized * diff
        self.fitness = self.func(*self.position)

class TBLO():
    def __init__(self, pop_size, dimens, lb, ub, generations, fnc):
        self.pop_size = pop_size
        self.dimens = dimens
        self.lb = lb
        self.ub = ub
        self.generations = generations
        self.func = fnc

        #Generate initial population
        self.population = [Student(self.func, self.lb, self.ub, self.dimens) for i in range(self.pop_size)]
        self.solutions = []
        self.t = None

    def step(self):

        for i, student in enumerate(self.population):
            student.position, student.fitness = self.teacher_phase(student)
            student.position, student.fitness = self.student_phase(student, i)

        #SORT BEFORE APPENDING to global solutions var = teacher is on pos with index 0
        self.population.sort(key = operator.attrgetter('fitness'), reverse = False)
        
        self.solutions.append(copy.deepcopy(self.population))
        self.t = self.get_teacher()

    def get_teacher(self):
        best = min(self.population, key=attrgetter('fitness'))

        return best

    def teacher_phase(self, student):
        teacher = self.get_teacher()
        tf = np.random.randint(1, 2)
        c = np.zeros(self.dimens)

        for i, position in enumerate(student.position):
            s_mean = np.mean([s.position[i] for s in self.population])

            r = np.random.uniform(0, 1)
            diff_mean = teacher.position[i] - (tf * s_mean)

            c[i] = position + (r * diff_mean)

        best, best_fitness = self.select_best(student.position, c)

        return (best, best_fitness)

    def student_phase(self, student, student_index):
        k_index = self.random_learner_excluding([student_index])
        st = self.population[k_index]
        c = np.zeros(self.dimens)
        
        for i, position in enumerate(student.position):
            if student.fitness < st.fitness:
                diff = position - st.position[i]
            else:
                diff = st.position[i] - position

            r = np.random.uniform(0, 1)
            c[i] = position + (r * diff)

        best, best_fitness = self.select_best(student.position, c)

        return (best, best_fitness)

    def random_learner_excluding(self, excluded):
        available = set(range(self.pop_size))
        exclude = set(excluded)

        diff = available - exclude

        return np.random.choice(list(diff))

    def fitness(self, position):
        return self.func(*position)

    def select_best(self, s_position, c_position):
        s_fit = self.fitness(s_position)
        c_fit = self.fitness(c_position)

        if s_fit > c_fit:
            best = c_position
            best_fitness = c_fit
        else:
            best = s_position
            best_fitness = s_fit
        #print("s_fit: ", s_fit, " c_fit: ", c_fit)
        return (best, best_fitness)

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

            ax.plot_surface(X, Y, Z, alpha=0.35, cmap=cm.binary, linewidth=0.1, antialiased=True)
            ax.set_xlim([self.lb, self.ub])
            ax.set_ylim([self.lb, self.ub])

            first = True
            for j in self.solutions[i]:
                if first:
                    #Marking the best one (first)
                    ax.plot(j.position[0], j.position[1], self.func(j.position[0], j.position[1]), 'go')
                else:
                    ax.plot(j.position[0], j.position[1], self.func(j.position[0], j.position[1]), 'bo', alpha=0.25)
                first = False

            plt.pause(0.05)
        
        plt.show()

    def run(self):
        for i in range(self.generations):
            self.step()
            print('[' + str(i) +'] Teacher best fitness and position is: \t' + str(self.t.fitness) + '\t | ' + str(self.t.position))

        self.visualize()


if __name__ == "__main__":
    #Parameters
    p_pop_size = 30
    p_dimens = 2
    p_lb = -32.768
    p_ub = 32.768
  
    p_generations = 30
    p_func = sphere

    tblo = TBLO(p_pop_size, p_dimens, p_lb, p_ub, p_generations, p_func)
    tblo.run()