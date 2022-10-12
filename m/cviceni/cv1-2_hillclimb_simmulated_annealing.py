import numpy as np
 
from numpy import abs, cos, exp, mean, pi, prod, sin, sqrt, sum
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

    return np.sum(sum1)

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

def hillClimb(start_coords, func, d, calcMin = True):
    global g_maximal, neighbors_count, sigma

    runned = []
    runnedZs = []


    #Save operator for finding global min or max
    if calcMin:
         comp = operator.lt
    else:
        comp = operator.gt

    #Calculate value for starting points and set default X and Y for next iteration
    xb = func(*start_coords)
    xb_vector = start_coords

    #Dynamically count length of given start coords
    size = len(start_coords)
    #Repeat X generations
    for gen in range(0, g_maximal):
        #Repeat NP times for each neighbors location
        if calcMin:
            xs = np.Inf
        else:
            xs = 0
        xs_vector = []

        for i in range(neighbors_count):
            generated = []
            for ii in range(size):
                generated.append(np.random.normal(xb_vector[ii], sigma))
            val = func(*generated)
            #Save the best one accord to min/max
            #If true, save the X and Y and its value as new max/min
            if comp(val, xs):
                xs = val
                xs_vector = generated

        #After all, compare start value with the newest value, if its lower/greater, go to next iteration (using recursive fnc)
        if comp(xs, xb):
            xb = xs
            xb_vector = xs_vector
            runned.append(xs_vector)
            runnedZs.append(xs)

        #For debugging
        if gen % 100 == 0:
            print("I'm now running generation number", gen, " with max/min value: ", xb, ".")
    
    if calcMin:
        print('Minimum found as:', xb)
    else:
        print('Maximum found as:', xb)

    fnc = np.vectorize(func)
    draw(-4, 4, fnc, runned, runnedZs)
    return xb


def simulatedAnnealing(t0, t_min, alpha, fnc, lb, ub, dimens, sigma):
    t = t0
    runned = []
    runnedZs = []

    #Generate starting coords
    x = []
    for i in range(dimens-1):
        x.append(random.randint(lb, ub))

    #Evaluate it
    x_val = fnc(*x)

    #Main loop
    while t > t_min:
        #Neighbour coords generation
        x1 = []
        for i in range(len(x)):
            x1.append(np.random.normal(x[i], sigma))

        #Eval neighbour
        x1_val = fnc(*x1)

        if(x1_val < x_val):
            x = x1
            x_val = x1_val

            #For visualization only
            runned.append(x1)
            runnedZs.append(x1_val)
        else:
            #Generate random val between 0 and 1
            r = random.uniform(0, 1)
            e = math.exp(-(x1_val - x_val) / t)

            print(r, ",", e)
            if r < e:
                x = x1
                x_val = x1_val

                #For visualization only
                runned.append(x1)
                runnedZs.append(x1_val)

        t *= alpha
        print("Tecko: ",t)
    #Visualize the func at the end
    func = np.vectorize(fnc)
    draw(lb, ub, func, runned, runnedZs)



def updatePoints(n, x, y, z, point):
    point.set_data(np.array([x[n], y[n]]))
    point.set_3d_properties(z[n], 'z')
    return point


def draw(lw, ub, fnc, points, z):
    fig = plt.figure()
    ax = ax3.Axes3D(fig)

    X = np.linspace(lw, ub, 200)
    Y = np.linspace(lw, ub, 200)
    X, Y = np.meshgrid(X, Y)
    Z = fnc(X, Y)
    ax.plot_surface(X, Y, Z, alpha=0.6, cmap=cm.OrRd, linewidth=0.1, antialiased=True)

    #Doing animation
    x = []
    y = []

    for i in range(len(points)):
        x.append(points[i][0])
        y.append(points[i][1])

    point, = ax.plot(x[0], y[0], z[0], 'go')
    animation = anim.FuncAnimation(fig, updatePoints, len(x), interval=250, fargs=(x, y, z, point), repeat=False)
    plt.show()

#Global variables
upper_bound = 10
lower_bound = -10
g_maximal = 500
lw = -4
g_maximal = 500
neighbors_count = 5
sigma = 0.5
t0 = 100
t_min = 0.3
alpha = 0.95
start_coords = [upper_bound, upper_bound]

# hillClimb(start_coords, sphere, 2, True)
simulatedAnnealing(t0, t_min, alpha, michalewicz, lower_bound, upper_bound, 3, sigma)
