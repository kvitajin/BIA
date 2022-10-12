from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
# import matplotlib.animation as wanimation
from matplotlib import cm
# from pl toolkits.mplot3d import Axes3D
import numpy as np
import operator
import mpl_toolkits.mplot3d.axes3d as ax3
import matplotlib.animation as anim



def sphere(parameters):
    tmp = 0
    for i in parameters:
        tmp += i*i
    return tmp


def ackley(parameters, a=20, b=0.2, c=2*np.pi):
    sum1 = sphere(parameters)
    sum2 = 0
    for i in parameters:
        sum2 += np.cos(c*i)
    return -a*np.exp(-b * np.sqrt(sum1 / len(parameters))) - np.exp(sum2/len(parameters)) + np.exp(1)


def rastrigin(parameters):
    tmp=0
    for i in parameters:
        tmp += i*i-10*np.cos(2*np.pi*i)
    return 10*len(parameters) + tmp


def rosenbrock(parameters):
    n = len(parameters)-1
    tmp= 0
    for i in range(n):
        tmp += 100*(parameters[i+1]-parameters[i]*parameters[i])**2 + (parameters[i]-1)**2
    return tmp


def griewank(parameters):
    tmp1 = 0
    tmp2 = 1
    counter = 1
    for i in parameters:
        tmp1 += i*i/4000
        tmp2 *= np.cos(i/np.sqrt(counter))
        counter += 1
    return tmp1 - tmp2 + 1


def schwefel(*parameters):
    tmp = 1
    for i in parameters:
        tmp += i*np.sin(np.sqrt(np.abs(i)))
    return 418.9829*len(parameters)-tmp


def lewiiii(i):
    return 1 + (i-1)/4


def levy(parameters):
    n=len(parameters)-2
    tmp = 0
    for i in range(n):
        tmp += (lewiiii(parameters[i])-1)**2 * (1+10*(np.sin(np.pi*lewiiii(parameters[i])+1)**2))
    return (np.sin(np.pi*lewiiii(parameters[0])))**2 + tmp + \
           (((lewiiii(parameters[n+1])-1)**2)*(1+(np.sin(2*np.pi*lewiiii(parameters[n+1])))**2))


def michalewicz(parameters, m=10):
    counter = 1
    tmp = 0
    for i in parameters:
        tmp += np.sin(i)*(np.sin(counter*(i**2)/np.pi))**(2*m)
        counter += 1
    return -tmp


def zakharov(parameters):
    tmp = 0
    tmp2 = 0
    counter = 1
    for i in parameters:
        tmp += i**2
        tmp2 += 0.5 * counter*i
        counter += 1
    return tmp + tmp2**2 + tmp2**4


def make_surface(func, xmin, xmax, ymin, ymax, step):
    X = np.arange(xmin, xmax, step)
    Y = np.arange(ymin, ymax, step)
    Z = []

    for x in X:
        temparr = []
        for y in Y:
            temparr.append(func([x, y]))
        Z.append(np.array(temparr))
    X, Y = np.meshgrid(X, Y)
    Z = np.array(Z)
    return X, Y, Z


def update_frame(i, data, scat, ax):
    #print("frame {e}".format(i))
    scat[0].remove()
    #scat[0] = ax[0].scatter(*data[i], c='red')
    scat[0]= ax[0].scatter([x[0] for x in data[i]], [y[i] for y in data[i]], [z[2] for z in data[i]], c='red')
    print('frame {0}'.format(i))


def init_frame():
    print("repeat")


def render_anim(X, Y, Z, data=[], name="", save=True):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    # ax = Axes3D (fig)
    if len(name) > 0:
        ax.set_title(name)
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False, alpha=.9)
    if len(data) > 0:
        i = 0
        scat = ax.scatter([x[0] for x in data[i]], [y[1] for y in data[i]], [z[2] for z in data[i]], c='red')
        animation = FuncAnimation(fig, update_frame, len(data), fargs=(data, [scat], [ax]), init_func=init_frame)
        if save and len(name) > 0:
            Writer = wanimation.writers['ffmpeg']
            writer = Writer(fps=5, metadata=dict(artist='Me'), bitrate=1000, extra_args=['-vcodec', 'libx264'])
            animation.save('{0}.mp4'.format(name), writer=writer)
    plt.show()


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


def updatePoints(n, x, y, z, point):
    point.set_data(np.array([x[n], y[n]]))
    point.set_3d_properties(z[n], 'z')
    return point

def hillClimb(rozsah, func, d, calcMin=True):
    global g_maximal, neighbors_count, sigma

    runned = []
    runnedZs = []

    # Save operator for finding global min or max
    if calcMin:
        comp = operator.lt
    else:
        comp = operator.gt

    # Calculate value for starting points and set default X and Y for next iteration
    xb = func(*rozsah)
    xb_vector = rozsah

    # Dynamically count length of given start coords
    size = len(rozsah)
    # Repeat X generations
    for gen in range(0, iterations):
        # Repeat NP times for each neighbors location
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
            # Save the best one accord to min/max
            # If true, save the X and Y and its value as new max/min
            if comp(val, xs):
                xs = val
                xs_vector = generated

        # After all, compare start value with the newest value, if its lower/greater, go to next iteration (using recursive fnc)
        if comp(xs, xb):
            xb = xs
            xb_vector = xs_vector
            runned.append(xs_vector)
            runnedZs.append(xs)

        # For debugging
        if gen % 100 == 0:
            print("I'm now running generation number", gen, " with max/min value: ", xb, ".")

    if calcMin:
        print('Minimum found as:', xb)
    else:
        print('Maximum found as:', xb)

    fnc = np.vectorize(func)
    draw(-4, 4, fnc, runned, runnedZs)
    return xb


# def calcZ(X, Y, function):
#     Z = np.zeros((len(X), len(Y)))
#     for i in range(len(X)):
#         for j in range(len(Y)):
#             Z[i, j] = function([X[i], Y[j]])
#     return Z
# #
#
# def pokus():
#     iterations = 500
#     dimensions = 2
#     function = zakharov
#     rozsah = rozsahy(function)
#     points_per_iteration = 10
#
#     minimum = float("inf")
#
#     min_x = np.array([])
#     min_y = np.array([])
#     min_z = np.array([])
#
#     plt.ion()
#     fig = plt.figure()
#     ax = fig.add_subplot(projection='3d')
#     step = (rozsah[1]-rozsah[0])/1000
#     X = np.arange(rozsah[0], rozsah[1], step)
#     Y = np.arange(rozsah[0], rozsah[1], step)
#     Z = calcZ(X, Y, function)
#     Y, X = np.meshgrid(X, Y)
#     ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, alpha=0.9)
#     plt.show()
#     for i in range(len(min_x)):
#         ax.scatter(min_x[i], min_y[i], min_z[i], c="#0000FF")
#         plt.pause(0.01)
#     plt.show(block=True)


def rozsahy(function):
    if function == sphere:          #krater
        return -5.12, 5.12
    elif function == rosenbrock:    #u rampa
        return -10, 10
    elif function == griewank:      #vlnky/krater/neco dalsiho
        return -50, 50
    elif function == schwefel:      #obsah kyblu po stredecni party
        return -500, 500
    elif function == levy:          #vlnena u rampa
        return -10, 10
    elif function == michalewicz:   #tektonicke pohyby
        return 0, np.pi
    elif function == zakharov:      #skokanek
        return -10, 10
    else:
        return 0, 0

if __name__ == '__main__':
    iterations = 500
    neighbors_count = 5
    sigma = 0.5
    rozsah = rozsahy(schwefel)
    hillClimb(rozsah, schwefel, 2, True)

# pokus()
    # rozsah = rozsahy(schwefel)
    # x, y, z = make_surface(schwefel, rozsah[0], rozsah[1], rozsah[0], rozsah[1], (rozsah[1]-rozsah[0])/1000)
    # render_anim(x, y, z, name="schwefel", data=[1,1], save=True)
