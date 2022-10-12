import threading
from numpy import arange
from numpy import linspace
from numpy import exp
from numpy import sqrt
from numpy import cos
from numpy import e
from numpy import pi
from numpy import meshgrid
import matplotlib.pyplot as plt
import time

from Function import *
from Solution import *
#from AckleyFunction import *
#from SphereFunction import *
#from Solution import *

def main():
	ackley = Function('ackley')
	griewank = Function('griewank')
	levy = Function('levy')
	michalewicz = Function('michalewicz')
	rastrigin = Function('rastrigin')
	rosenbrock = Function('rosenbrock')
	schwefel = Function('schwefel')
	sphere = Function('sphere')
	zakharov = Function('zakharov')

	#xaxis = linspace(-2, 2)
	#yaxis = linspace(-2, 2)
	#xaxis = arange(-f_range, f_range, step)
	#yaxis = arange(-f_range, f_range, step)
	#x, y = meshgrid(xaxis, yaxis)

	#results = sphere.sphere([x, y])
	#results = ackley.ackley([x, y])
	#results = griewank.griewank([x, y])
	#results = levy.levy([x, y])
	#results = michalewicz.michalewicz([x, y])
	#results = rastrigin.rastrigin([x, y])
	#results = rosenbrock.rosenbrock([x, y])
	#results = schwefel.schwefel([x, y])
	#results = zakharov.zakharov([x, y])

	solution = Solution(2, -20, 20)
	#solution.hill_climb(sphere, 8, 0.5)
	#solution.simulated_annealing(sphere)
	#solution.evolution(sphere, 20, 100)
	#solution.trading_salesman([
	#	#Prag, Berl, Buda, Mosc, Anka, Brat
	#	[   0,  349,  525, 1932, 2291,  328], #Prag
	#	[ 349,    0,  873, 1826, 2640,  677], #Berl
	#	[ 525,  873,    0, 2113, 1775,  201], #Buda
	#	[1932, 1826, 2113,    0, 2420, 1917], #Mosc
	#	[2291, 2640, 1775, 2420,    0, 1967], #Anka
	#	[ 328,  677,  201, 1917, 1967,    0], #Brat
	#], 10, 100, 0.5)
	#solution.differential(sphere)
	#solution.particle_swarm(sphere, 15, 100)
	#solution.soma(sphere, 10, 100)
	#solution.ant_colony(20, 100, 1.0, 2.0, 0.5, 1.0)
	#solution.firefly(sphere, 5, 10)
	solution.teaching(sphere)
	#solution.hill_climb(ackley, 8, 0.5)
	#solution.hill_climb(griewank, 8, 0.5)
	#solution.hill_climb(levy, 8, 0.5)
	#solution.hill_climb(michalewicz, 8, 0.5)
	#solution.hill_climb(rastrigin, 8, 0.5)
	#solution.hill_climb(rosenbrock, 8, 0.5)
	#solution.hill_climb(schwefel, 8, 0.5)
	#solution.hill_climb(zakharov, 8, 0.5)

	#figure = plt.figure()
	#axis = figure.gca(projection = '3d')
	#axis.plot_surface(x, y, results, cmap = 'jet', shade = 'false')
	#plt.show()

	#plt.contour(x,y,results)
	#plt.show()

	#plt.scatter(x, y, results)
	#plt.show()

if __name__ == '__main__':
	main()
