import numpy as np

import mpl_toolkits.mplot3d.axes3d as ax3
import matplotlib.animation as anim

import random, operator
from matplotlib import cm
import matplotlib.pyplot as plt

import math

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

def differentialEvolution(func, lb, ub, dimens, f, cr, n, g):
    #Generate normalized population
    pop = np.random.rand(n, dimens)

    #Denormalize the population
    diff = np.fabs(lb - ub)
    pop_denorm = lb + pop * diff

    #Calculate values and create array
    fitness = np.asarray([func(*i) for i in pop_denorm])

    #Find lowest value (index + points)
    best_index = np.argmin(fitness)
    best = pop_denorm[best_index]
    pnts = []

    for i in range(g):
        gpnts = []
        for j in range(n):
            #Select 3 random from population, except the one which is iterating at the time
            indexes = [k for k in range(n) if k != j]
            r1, r2, r3 = pop[np.random.choice(indexes, 3, replace = False)]

            #Limit normalized value between (0, 1) - checking bounds
            v = np.clip(r1 + f * (r2 - r3), 0, 1)

            #Generate crossover points
            j_rnd = np.random.rand(dimens) < cr
            if not np.any(j_rnd):
                j_rnd[np.random.randint(0, dimens)] = True

            #Generate new mutation vector
            u = np.where(j_rnd, v, pop[j])

            #Denormalize and calculate the value
            u_denorm = lb + u * diff
            f_u = func(*u_denorm)

            #Compare the value of mutant with target vector
            if f_u <= fitness[j]:
                fitness[j] = f_u
                pop[j] = u

                gpnts.append(u_denorm)

                if f_u < fitness[best_index]:
                    best_index = j
                    best = u_denorm

        pnts.append(gpnts)

    #Visualize function with calculated points
    visualize(func, lb, ub, pnts)

def visualize(func, lb, ub, points):
    fig = plt.figure()
    ax = fig.subplots()
    X = np.linspace(lb, ub, 200)
    Y = np.linspace(lb, ub, 200)
    X, Y = np.meshgrid(X, Y)
    Z = func(X, Y)

    #For each gen
    for i in points:
        ax.clear()

        ax.pcolormesh(X, Y, Z.reshape(X.shape), shading='gouraud', cmap=cm.plasma)
        ax.set_xlim([lb, ub])
        ax.set_ylim([lb, ub])

        for j in i:
            ax.plot(j[0], j[1], 'ko')

        plt.pause(0.05)
    
    plt.show()


if __name__ == "__main__":
    differentialEvolution(sphere, -20, 20, 2, 0.5, 0.5, 10, 50)
