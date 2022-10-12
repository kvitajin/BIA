from random import randint, random

import time
import numpy
from numpy import exp
from numpy import e
import mpl_toolkits.mplot3d.axes3d as p3
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import copy

def print_matrix(matrix):
	for row in matrix:
		print('|   ', end='')
		for col in row:
			print('%.5f   ' % (col), end='')
		print('|')

def print_params(params: list) -> str:
	for i in range(len(params)):
		print('%.2f' % (params[i],), end='')
		if i < len(params) - 1:
			print(', ', end='')
	return ''

class Solution:
	def __init__(self, dimension, lower_bound, upper_bound):
		"""Solution constructor
			lower and upper bound will be used for all dimensions
		"""

		self.dimension = dimension
		self.lower_bound = lower_bound
		self.upper_bound = upper_bound
		self.parameters = numpy.zeros(self.dimension) #solution parameters
		self.function = numpy.inf #objective function evaluation

	def get_random_solution(self, function = None, offset = 0):
		result = numpy.random.uniform(self.lower_bound + offset, self.upper_bound - offset, self.dimension).tolist()
		if function:
			result.append(function(result))
		return result

	def check_bounds(self, params: list) -> bool:
		for i in range(len(params)):
			if (i == self.dimension):
				break
			if params[i] < self.lower_bound:
				params[i] = self.lower_bound
			elif params[i] > self.upper_bound:
				params[i] = self.upper_bound

	def update_points(self, n, x, y, z, point):
		point.set_data(numpy.array([x[n], y[n]]))
		point.set_3d_properties(z[n], 'z')
		return point

	def vizualize(self, points, function):
		fig = plt.figure()
		ax = p3.Axes3D(fig)
		x = []
		y = []
		z = []

		self.draw(self.lower_bound, self.upper_bound, function, ax)
		for i in range(len(points)):
			x.append(points[i][0])
			y.append(points[i][1])
			z.append(points[i][2])
		point, = ax.plot(x[0], y[0], z[0], '^')
		animate = animation.FuncAnimation(fig, self.update_points, len(x), interval = 50, fargs = (x, y, z, point), repeat=False)
		plt.show()

	def draw(self, min, max, function, ax):
		X = numpy.linspace(min, max)
		Y = numpy.linspace(min, max)
		X, Y = numpy.meshgrid(X, Y)
		Z = function([X, Y])
		ax.plot_surface(X, Y, Z, cmap = 'jet', shade = 'true', alpha=0.2)

	def generate_neighbours(self, params: list, neighbour_count, sigma) -> list:
		"""generate_neighbours returns neighbours generated by gauss method"""
		neighbours = []
		print('gen neib', params)
		for i in range(neighbour_count):
			neighbour = []

			for param in params:
				valid = False
				while not valid:
					value = numpy.random.normal(param, sigma)

					if value >= self.lower_bound and value <= self.upper_bound:
						neighbour.append(value)
						valid = True

			neighbours.append(neighbour)
		return neighbours

	def hill_climb(self, function, neighbour_count = 8, sigma = 0.5, iteration_limit = 500) -> list:
		"""hill_climb returns lowest point in specified function"""
		best_points = []
		#best_point = self.get_random_solution()
		best_point = [self.upper_bound, self.upper_bound]
		z = function(best_point)
		best_point.append(z)

		for i in range(iteration_limit):
			print('-bp-| x: %f y: %f z: %f' % (best_point[0], best_point[1], best_point[2]))
			best_points.append(best_point)
			neighbours = self.generate_neighbours([best_point[0], best_point[1]], neighbour_count, sigma)
			found_better_point = False

			for neighbour in neighbours:
				z = function(neighbour)
				print(' nb | x: %f y: %f z: %f' % (neighbour[0], neighbour[1], z))

				if z < best_point[2]:
					found_better_point = True
					best_point = [neighbour[0], neighbour[1], z]

			if not found_better_point:
				self.vizualize(best_points, function)
				return best_point, True

		self.vizualize(best_points, function)
		return best_point, False

	def simulated_annealing(self, function, temperature_0 = 100, temperature_min = 0.5, alpha = 0.95, sigma = 0.5):
		temperature = temperature_0
		best_points = []
		#best_point = self.get_random_solution()
		best_point = [self.upper_bound, self.upper_bound]
		z = function(best_point)
		best_point.append(z)
		best_points.append(best_point)
		count = 0
		count_2 = 0

		while temperature > temperature_min:
			#print('-bp-| x: %f y: %f z: %f' % (best_point[0], best_point[1], best_point[2]))
			neighbour = self.generate_neighbours([best_point[0], best_point[1]], 1, sigma)[0]
			z = function(neighbour)
			#print(' nb | x: %f y: %f z: %f' % (neighbour[0], neighbour[1], z))

			if z < best_point[2]:
				best_point = [neighbour[0], neighbour[1], z]
				best_points.append(best_point)
			else:
				r = numpy.random.uniform()
				z_diff = z - best_point[2]
				print('old z: %f new z: %f diff: %f' % (z, best_point[2], z_diff))
				#print('temp: %f diff/temp: %f, r: %f exp: %f' % (temperature, -(z_diff / temperature), r, e**(-(z_diff / temperature))))
				if r > e**(-(z_diff / temperature)):
					count += 1
					best_point = [neighbour[0], neighbour[1], z]
					best_points.append(best_point)
				else:
					count_2 += 1

			temperature = temperature * alpha

		#print('worse accepted:', count)
		#print('worse refused:', count_2)

		self.vizualize(best_points, function)
		return best_point, False

	def evolution(self, function, parents_count = 20, iteration_count = 1000, sigma = 0.5):
		best_points = []
		offspring = []
		for i in range(parents_count):
			parent = self.get_random_solution(function)
			offspring.append(parent)
		offspring.sort(key = lambda a: a[2])
		best_points.append(offspring[0])
		p = parents_count / 5.0

		for i in range(iteration_count):
			print('g[%i]:' % (i,), offspring[0])
			better_children_count = 0
			for j in range(parents_count):
				child = self.generate_neighbours(offspring[j][:2], 1, sigma)[0]
				child.append(function(child))
				offspring.append(child)

				if child[2] < offspring[j][2]:
					better_children_count += 1

			offspring.sort(key = lambda a: a[2])
			offspring = offspring[:parents_count]
			best_points.append(offspring[0])

			if better_children_count < p:
				sigma = sigma * 0.817
			elif better_children_count > p:
				sigma = sigma / 0.817

		self.vizualize(best_points, function)
		return offspring

	def trading_salesman(self, towns : list, parents_count = 20, iteration_count = 1000, mutation = 0.5):
		population = []
		towns_length = len(towns)
		path_length = towns_length + 1
		split_index = int(numpy.ceil(path_length / 2.0))

		if parents_count < 1:
			parents_count = 1

		for i in range(parents_count):
			child = [0]
			for j in range(towns_length - 1):
				town_index = 0
				while town_index in child:
					town_index = numpy.random.randint(1, towns_length)
				child.append(town_index)
			child.append(0)
			population.append(child)

		def get_value(child):
			sum = 0
			from_town = 0
			for i in range(len(child)):
				sum += towns[from_town][child[i]]
				from_town = child[i]
			return sum

		def cross_over(a, b):
			a_part = a[1:split_index]
			b_part = b[split_index:-1]

			j = 1
			for i in range(len(b_part) - 1, -1, -1):
				while b_part[i] in a_part:
					b_part[i] = b[split_index - j]
					j += 1
			return [0] + a_part + b_part + [0]

		def mutate(a):
			first_index = numpy.random.randint(1, len(a) - 1)
			second_index = numpy.random.randint(1, len(a) - 1)
			while second_index == first_index:
				second_index = numpy.random.randint(1, len(a) - 1)
			tmp = a[first_index]
			a[first_index] = a[second_index]
			a[second_index] = tmp

		best_population = []

		for i in range(iteration_count):
			new_population = population.copy()
			for j in range(parents_count):
				parent_1 = population[j]
				parent_2_index = numpy.random.randint(0, towns_length)
				while parent_2_index == j:
					parent_2_index = numpy.random.randint(0, towns_length)
				parent_2 = population[parent_2_index]
				offspring = cross_over(parent_1, parent_2)

				if numpy.random.uniform() < mutation:
					mutate(offspring)
				if get_value(offspring) < get_value(parent_1):
					new_population[j] = offspring
			best = None
			for item in new_population:
				value = get_value(item)
				if best is None or value < get_value(best):
					best = item
			population = new_population
			best_population.append(best)

		def update_points(num, data, line):
			x = numpy.arange(0, towns_length + 1)
			line.set_xdata(x)
			line.set_ydata(numpy.array(data[num]))
			return line

		print(best_population[-1], get_value(best_population[-1]))
		figure = plt.figure()
		l, = plt.plot(numpy.array([0, 1, 2, 3, 4, 5, 6]), numpy.array([0, 0, 0, 0, 0, 0, 0]))
		plt.ylim(0, towns_length + 2)
		animate = animation.FuncAnimation(figure, update_points, len(best_population), interval = 50, fargs=(best_population, l), repeat=False)
		plt.show()

	def differential(self, function, parents_count = 20, iteration_count = 100, F = 0.5, CR = 0.7):
		best_points = []
		population = []
		for i in range(parents_count):
			parent = self.get_random_solution(function)
			population.append(parent)
		population.sort(key = lambda a: a[2])
		best_points.append(population[0])

		def mutate(x, F):
			return numpy.array(x[0]) + F * (numpy.array(x[1]) - numpy.array(x[2]))

		def crossover(mutated, target, cr):
			p = self.get_random_solution()
			trial = []
			i_rnd = numpy.random.randint(0, self.dimension)
			for i in range(len(p)):
				if p[i] < cr or i == i_rnd:
					trial.append(mutated[i])
				else:
					trial.append(target[i])
			trial.append(function(trial))
			return trial

		for i in range(iteration_count):
			new_population = copy.deepcopy(population)

			for (index, item) in enumerate(population):
				r1 = numpy.random.randint(0, parents_count)
				while r1 == index:
					r1 = numpy.random.randint(0, parents_count)
				r2 = numpy.random.randint(0, parents_count)
				while r2 in [index, r1]:
					r2 = numpy.random.randint(0, parents_count)
				r3 = numpy.random.randint(0, parents_count)
				while r3 in [index, r1, r2]:
					r3 = numpy.random.randint(0, parents_count)

				mutated = mutate([population[r1], population[r2], population[r3]], F)
				for i in range(self.dimension):
					if mutated[i] < self.lower_bound:
						mutated[i] = self.lower_bound
					elif mutated[i] > self.upper_bound:
						mutated[i] = self.upper_bound

				trial = crossover(mutated, item, CR)

				if trial[self.dimension] <= item[self.dimension]:
					new_population[index] = trial
			population = new_population
			best = None
			for item in population:
				if best is None or item[self.dimension] < best[self.dimension]:
					best = item
			best_points.append(best)

		self.vizualize(best_points, function)

	def particle_swarm(
		self,
		function,
		migration_size = 20,
		migration_count = 100,
		v_min = None,
		v_max = None,
		c1 = 2.0,
		c2 = 2.0,
		w_s = 0.9,
		w_e = 0.4
	):
		if v_min is None:
			v_min = self.lower_bound / 20
		if v_max is None:
			v_max = self.upper_bound / 20

		global_best = None
		swarm = []
		swarms = []

		for i in range(migration_size):
			position = numpy.array(self.get_random_solution(function))
			velocity = numpy.random.uniform(v_min, v_max, self.dimension + 1)
			best = position.copy()
			swarm.append({ 'position': position, 'velocity': velocity, 'best': best })

			if global_best is None or best[self.dimension] < global_best[self.dimension]:
				global_best = best

		swarms.append(swarm)
		#for i, particle in enumerate(swarm):
		#	print('[Z][%i]' % (i,), particle['position'], particle['velocity'])

		for i in range(migration_count):
			swarm = copy.deepcopy(swarm)
			for (index, particle) in enumerate(swarm):
				inertia_weight = w_s - ((w_s - w_e) * index) / migration_count
				particle['velocity'] = (
					particle['velocity'] * inertia_weight +
					numpy.random.uniform(0, 1) * c1 * (particle['best'] - particle['position']) +
					numpy.random.uniform(0, 1) * c2 * (global_best - particle['position'])
				)
				for (index2, item2) in enumerate(particle['velocity']):
					if item2 < v_min:
						particle['velocity'][index2] = v_min
					elif item2 > v_max:
						particle['velocity'][index2] = v_max

				particle['position'] += particle['velocity']
				for (index3, item3) in enumerate(particle['position']):
					if item3 < self.lower_bound:
						particle['position'][index3] = self.lower_bound
					elif item3 > self.upper_bound:
						particle['position'][index3] = self.upper_bound
				particle['position'][self.dimension] = function(particle['position'][:2])

				if particle['position'][self.dimension] <= particle['best'][self.dimension]:
					particle['best'] = particle['position'].copy()

					if particle['best'][self.dimension] <= global_best[self.dimension]:
						global_best = particle['best'].copy()
			swarms.append(swarm)

		fig, ax = plt.subplots()
		X = numpy.linspace(self.lower_bound - 5, self.upper_bound + 5)
		Y = numpy.linspace(self.lower_bound - 5, self.upper_bound + 5)
		X, Y = numpy.meshgrid(X, Y)
		Z = function([X, Y])
		plt.contourf(X, Y, Z)
		sc = ax.scatter([], [], marker = (10, 0))

		def update_plot(i, data, sc):
			positions = []
			for particle in data[i]:
				positions.append(particle['position'][:2])
			sc.set_offsets(positions)

		animate = animation.FuncAnimation(fig, update_plot, len(swarms), fargs=(swarms, sc), interval = 100, repeat=False)
		plt.show()

	def soma(
		self,
		function,
		migration_size = 20,
		migration_count = 100,
		step = 0.11,
		path_length = 3,
		prt = 0.4
	):
		global_best = None
		swarm = []
		swarms = []
		for i in range(migration_size):
			position = numpy.array(self.get_random_solution(function))
			swarm.append(position)

			if global_best is None or position[self.dimension] <= global_best[self.dimension]:
				global_best = position
		swarms.append(swarm)

		iteration_count = int(numpy.floor(path_length / step))

		for i in range(migration_count):
			swarm = copy.deepcopy(swarm)
			for (index, particle) in enumerate(swarm):
				if numpy.array_equal(particle, global_best):
					continue

				prt_vector = []
				for j in range(self.dimension):
					if numpy.random.uniform() < prt:
						prt_vector.append(0)
					else:
						prt_vector.append(1)
				prt_vector.append(0)
				prt_vector = numpy.array(prt_vector)

				direction_vector = (global_best - particle) * prt_vector
				direction_vector /= numpy.sqrt(numpy.sum(direction_vector**2))
				current_best = particle.copy()

				for k in range(iteration_count):
					step_by = (k + 1) * step * direction_vector
					new_position = particle + step_by
					new_position[self.dimension] = function(new_position[:self.dimension])

					if new_position[self.dimension] < current_best[self.dimension]:
						current_best = new_position.copy()

				particle = current_best
				swarm[index] = particle

				if particle[self.dimension] <= global_best[self.dimension]:
					global_best = particle.copy()
			swarms.append(swarm)

		fig, ax = plt.subplots()
		X = numpy.linspace(self.lower_bound - 5, self.upper_bound + 5)
		Y = numpy.linspace(self.lower_bound - 5, self.upper_bound + 5)
		X, Y = numpy.meshgrid(X, Y)
		Z = function([X, Y])
		plt.contourf(X, Y, Z)
		sc = ax.scatter([], [], marker = (10, 0))

		def update_plot(i, data, sc):
			positions = []
			for particle in data[i]:
				positions.append(particle[:2])
			sc.set_offsets(positions)

		animate = animation.FuncAnimation(fig, update_plot, len(swarms), fargs=(swarms, sc), interval = 100, repeat=False)
		plt.show()

	def ant_colony(self, towns, iteration_count = 1000, alpha = 1.0, beta = 2.0, rho = 0.5, Q = 1.0):
		towns_pheromons = []
		towns_inverse_distance = []
		town_x = []
		town_y = []

		if towns is None or isinstance(towns, int):
			count = 20
			if isinstance(towns, int):
				count = towns
			towns = []

			for i in range(count):
				towns.append([])
				town_x.append(numpy.random.uniform(self.lower_bound, self.upper_bound))
				town_y.append(numpy.random.uniform(self.lower_bound, self.upper_bound))
			for y in range(count):
				for x in range(count):
					if x == y:
						towns[y].append(0)
						continue
					from_town = numpy.array([town_x[x], town_y[x]])
					to_town = numpy.array([town_x[y], town_y[y]])
					direction = from_town - to_town
					distance = numpy.absolute(numpy.sqrt(direction[0]**2 + direction[1]**2))
					towns[y].append(distance)
		else:
			for i in range(len(towns)):
				town_x.append(numpy.random.uniform(self.lower_bound, self.upper_bound))
				town_y.append(numpy.random.uniform(self.lower_bound, self.upper_bound))

		def get_value(children):
			sum = 0
			from_town = children[0]
			for index in range(len(children)):
				if index == 0:
					continue
				sum += towns[from_town][children[index]]
				from_town = children[index]
			return sum

		# prepare pheromons & inverse distance
		for i, row in enumerate(towns):
			towns_pheromons.append([])
			towns_inverse_distance.append([])

			for j, col in enumerate(row):
				towns_pheromons[i].append(rho)

				if col == 0:
					towns_inverse_distance[i].append(0)
				else:
					towns_inverse_distance[i].append(1.0 / col)

		#print('pheromone:')
		#print_matrix(towns_pheromons)
		#print('inverse:')
		#print_matrix(towns_inverse_distance)
		best_trajectories = []
		best_values = []

		plt.ion()

		for iteration in range(iteration_count):
			trajectories = []
			values = []

			for ant_index in range(len(towns)):
				#print('\nant:', ant_index)
				trajectory = []
				trajectory.append(ant_index)
				#print('trajectory:', ant_index)

				for town_index in range(len(towns) - 1):
					probabilities = []
					probability_town_indexes = []

					for destination_index in range(len(towns)):
						if destination_index in trajectory:
							continue
						pheromone_value = pow(towns_pheromons[trajectory[-1]][destination_index], alpha)
						inverse_distance_value = pow(towns_inverse_distance[trajectory[-1]][destination_index], beta)
						probabilities.append(pheromone_value * inverse_distance_value)
						probability_town_indexes.append(destination_index)

					sum = numpy.sum(probabilities)
					#if ant_index == 1 and town_index == 0:
					#	print('probabilities', probabilities)
					probabilities = numpy.array(probabilities) / sum
					random_value = numpy.random.uniform()
					chosen_town_index = None
					#if ant_index == 1 and town_index == 0:
					#	print('random: %.2f cumulative probabilities:' % (random_value,), probabilities)

					for probability_index, probability in enumerate(probabilities):
						if random_value < probability + numpy.sum(probabilities[:probability_index]):
							chosen_town_index = probability_town_indexes[probability_index]
							break
					trajectory.append(chosen_town_index)
					#print('trajectory:', chosen_town_index)
				trajectory.append(ant_index)
				value = get_value(trajectory)

				trajectories.append(trajectory)
				values.append(value)
				#print('trajectory:', trajectory, value)

				#for i in range(len(towns_pheromons)):
				#	for j in range(len(towns_pheromons[i])):
				#		towns_pheromons[i][j] *= rho
				#		towns_pheromons[i][j] += Q / value

			# vape it all
			for i in range(len(towns_pheromons)):
				for j in range(len(towns_pheromons[i])):
					towns_pheromons[i][j] *= rho

			#print('\nvaped pheromons:')
			#print_matrix(towns_pheromons)

			for trajectory_index, trajectory in enumerate(trajectories):
				previous_item = None

				for index, item in enumerate(trajectory):
					if index == 0:
						previous_item = item
						continue
					towns_pheromons[previous_item][item] += Q / values[trajectory_index]
					previous_item = item

			iteration_best = None

			for index, item in enumerate(values):
				if iteration_best is None or item < values[iteration_best]:
					iteration_best = index
				#print(trajectories[index], item)
			#print('')

			#print(trajectories[iteration_best], values[iteration_best])
			best_trajectories.append(trajectories[iteration_best])
			best_values.append(values[iteration_best])

			plt.clf()
			plt.scatter(town_x, town_y, s=60, alpha=0.5)
			best_index = None
			for index, item in enumerate(best_values):
				if best_index is None or item < best_values[best_index]:
					best_index = index
			best_trajectory = best_trajectories[best_index]
			previous_town_index = None
			#print(best_trajectory)

			for town_index in best_trajectory:
				if previous_town_index is None:
					previous_town_index = town_index
					continue
				plt.plot([town_x[previous_town_index], town_x[town_index]], [ town_y[previous_town_index], town_y[town_index]], color = 'r')
				previous_town_index = town_index

			plt.title('TSP Current:' + str(best_values[best_index]))
			plt.xlabel('X')
			plt.ylabel('Y')

			plt.draw()
			plt.pause(0.1)
			#print('iteration pheromons:')
			#print_matrix(towns_pheromons)
			#print('trajectory:', trajectories[iteration_best], values[iteration_best])
		time.sleep(5)

	def firefly(self, function, population_size = 20, iteration_count = 100, light_absorption = 2.0, alpha = 0.3, beta_0 = 1.0, sigma = 0.5):
		population = []
		populations = []
		best_fireflies = []

		for i in range(population_size):
			population.append(numpy.array(self.get_random_solution(function)))

		population.sort(key = lambda a: a[self.dimension])
		populations.append(copy.deepcopy(population))
		print('\npopulation:')
		for p in population:
			print('%.2f %.2f %.2f' % (p[0],p[1],p[2]))
		print('')

		for iteration_index in range(iteration_count):
			for i in range(population_size):
				if i == 0:
					continue
				for j in range(population_size):
					if (i == j):
						continue
					direction = population[j] - population[i]
					distance = numpy.absolute(numpy.sqrt(direction[0]**2 + direction[1]**2))
					#intensity = pow(population[i] * e, -light_absorption * distance)

					if population[j][self.dimension] < population[i][self.dimension]:
						beta = beta_0 / (1 + distance)
						#random_vector = self.generate_neighbours(population[j][:self.dimension], 1, sigma)[0]
						random_vector = self.generate_neighbours(beta * direction[:self.dimension], 1, sigma)[0]
						random_vector.append(0)
						random_vector = numpy.array(random_vector)
						#print('i:', end=' ')
						#print_params(population[i])
						#print(' j:', end=' ')
						#print_params(population[j])
						#print(' d:', end=' ')
						#print_params(direction * beta)
						#print(' r:', end=' ')
						#print_params(alpha * random_vector)
						#print('')
						population[i] = population[i] + beta * (direction) + alpha * random_vector
						self.check_bounds(population[i])
						population[i][self.dimension] = function(population[i][:self.dimension])
						#print('after: ', end='')
						#print_params(population[i])
						#print('')
			population.sort(key = lambda a: a[self.dimension])
			best_fireflies.append(population[0])
			populations.append(copy.deepcopy(population))
			#print('\npopulation:')
			#for p in population:
			#	print('%.2f %.2f %.2f' % (p[0],p[1],p[2]))
			print('best %i:' % (iteration_count), end=' ')
			print_params(population[0])
			print('')
		#self.vizualize(best_fireflies, function)

		fig, ax = plt.subplots()
		X = numpy.linspace(self.lower_bound - 5, self.upper_bound + 5)
		Y = numpy.linspace(self.lower_bound - 5, self.upper_bound + 5)
		X, Y = numpy.meshgrid(X, Y)
		Z = function([X, Y])
		plt.contourf(X, Y, Z)
		sc = ax.scatter([], [], marker = (10, 0))

		def update_plot(i, data, sc):
			positions = []
			for position in data[i]:
				positions.append(position[:2])
			sc.set_offsets(positions)

		animate = animation.FuncAnimation(fig, update_plot, len(populations), fargs=(populations, sc), interval = 100, repeat=False)
		plt.show()

	def teaching(self, function, children_count = 20, iteration_count = 100):
		children = []
		childrens = []

		for i in range(children_count):
			children.append(numpy.array(self.get_random_solution(function)))

		children.sort(key = lambda a: a[self.dimension])
		childrens.append(copy.deepcopy(children))

		for i in range(iteration_count):
			sum = numpy.zeros(self.dimension + 1)

			for child in children:
				sum += numpy.array(child)

			average = sum / children_count
			random_value_1 = numpy.random.uniform()
			random_value_2 = numpy.random.randint(1, 3)
			difference = numpy.random.uniform() * (children[0] - random_value_2 * average)
			new_teacher = children[0] + difference
			new_teacher[self.dimension] = function(new_teacher[:self.dimension])

			if new_teacher[self.dimension] < children[0][self.dimension]:
				children[0] = new_teacher

			for learner_index in range(1, len(children)):
				random_learner_index = numpy.random.randint(1, len(children))

				while random_learner_index == learner_index:
					random_learner_index = numpy.random.randint(1, len(children))

				new_child = None

				if children[learner_index][self.dimension] < children[random_learner_index][self.dimension]:
					new_child = children[learner_index] + random_value_1 * (children[learner_index] - children[random_learner_index])
				else:
					new_child = children[learner_index] + random_value_1 * (children[random_learner_index] - children[learner_index])

				new_child[self.dimension] = function(new_child[:self.dimension])

				if new_child[self.dimension] < children[learner_index][self.dimension]:
					children[learner_index] = new_child

			children.sort(key = lambda a: a[self.dimension])
			childrens.append(copy.deepcopy(children))

		fig, ax = plt.subplots()
		X = numpy.linspace(self.lower_bound - 5, self.upper_bound + 5)
		Y = numpy.linspace(self.lower_bound - 5, self.upper_bound + 5)
		X, Y = numpy.meshgrid(X, Y)
		Z = function([X, Y])
		plt.contourf(X, Y, Z)
		sc = ax.scatter([], [], marker = (10, 0))

		def update_plot(i, data, sc):
			positions = []
			for position in data[i]:
				positions.append(position[:2])
			sc.set_offsets(positions)

		animate = animation.FuncAnimation(fig, update_plot, len(childrens), fargs=(childrens, sc), interval = 100, repeat=False)
		plt.show()