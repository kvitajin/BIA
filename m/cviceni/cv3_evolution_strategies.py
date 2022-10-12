from contextlib import nullcontext
import numpy as np

from numpy import abs, cos, exp, mean, pi, prod, sin, sqrt, sum
import mpl_toolkits.mplot3d.axes3d as ax3
import matplotlib.animation as anim

import random
import operator
from matplotlib import cm
import matplotlib.pyplot as plt
import math

from numpy.random.mtrand import laplace

from numpy import asarray
from numpy import exp
from numpy import sqrt
from numpy import cos
from numpy import e
from numpy import pi
from numpy import argsort
from numpy.random import randn
from numpy.random import rand
from numpy.random import seed


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


def sphere(*params):
    sum1 = []

    for i in range(len(params)):
        sum1.append(params[i]**2)

    return np.sum(sum1)

# check if a point is within the bounds of the search


def in_bounds(point, bounds):
    # enumerate all dimensions of the point
    for d in range(len(bounds)):
        # check if out of bounds for this dimension
        if point[d] < bounds[d, 0] or point[d] > bounds[d, 1]:
            return False
    return True


# evolution strategy (mu + lambda) algorithm
def evolutionStrategies(objective, bounds, n_iter, step_size, mu, lam):
    # check if a point is within the bounds of the search
    best, best_eval = None, 1e+10
    # calculate the number of children per parent
    n_children = int(lam / mu)
    # initial population
    population = list()
    pop = []
    sco = []
    for _ in range(lam):
        candidate = None
        while candidate is None or not in_bounds(candidate, bounds):
            candidate = bounds[:, 0] + rand(len(bounds)) * (bounds[:, 1] - bounds[:, 0])
        population.append(candidate)
    # perform the search
    for epoch in range(n_iter):
        # evaluate fitness for the population
        scores = [objective(c) for c in population]
        # rank scores in ascending order
        ranks = argsort(argsort(scores))
        # select the indexes for the top mu ranked solutions
        selected = [i for i,_ in enumerate(ranks) if ranks[i] < mu]
        # create children from parents
        children = list()
        for i in selected:
            # check if this parent is the best solution ever seen
            if scores[i] < best_eval:
                best, best_eval = population[i], scores[i]
                #print('%d, Best: f(%s) = %.5f' % (epoch, best, best_eval))
            # keep the parent
            children.append(population[i])
            # create children for parent
            for _ in range(n_children):
                child = None
                while child is None or not in_bounds(child, bounds):
                    child = population[i] + randn(len(bounds)) * step_size
            children.append(child)
		# replace population with children
        population = children
        
        pop.append(population)
        sco.append(scores)
    
    func = np.vectorize(objective)
    print(len(pop))
    print(len(sco))
    
    draw(-5, 5, func, pop, sco)
    return [best, best_eval]


def updatePoints(i, x, y, z, point):
    point.set_data(np.asarray(x[i]), np.asarray(y[i]))
    point.set_3d_properties(np.asarray(z[i]))
    return point, 

def draw(lw, ub, fnc, points, z):
    fig = plt.figure()
    ax = ax3.Axes3D(fig)

    X = np.linspace(lw, ub, 200)
    Y = np.linspace(lw, ub, 200)
    X, Y = np.meshgrid(X, Y)
    Z = fnc(X, Y)
    ax.plot_surface(X, Y, Z, alpha=0.6, cmap=cm.OrRd, linewidth=0.1, antialiased=True)

    # Doing animation
    x = []
    y = []
    point = []
    pp = np.array(points)
    for i in range(0, len(points)):
        xx = []
        yy = []
        for j in pp[i]:
            xx.append(j[0])
            yy.append(j[1])
        x.append(xx)
        y.append(yy)

    point, = ax.plot(x[0], y[0], z[0], 'go')

    animation = anim.FuncAnimation(fig, updatePoints, len(x), interval=250, fargs=(x, y, z, point), repeat=False)
    plt.show()



if __name__ == "__main__":
    # seed the pseudorandom number generator
    np.random.seed(1)
    # define range for input
    bounds = np.asarray([[-5, 5], [-5, 5]])
    # define the total iterations
    n_iter = 10
    # define the maximum step size
    step_size = 0.15
    # number of parents selected
    mu = 20
    # the number of children generated by parents
    lam = 200

    evolutionStrategies(sphere, bounds, n_iter, step_size, mu, lam)