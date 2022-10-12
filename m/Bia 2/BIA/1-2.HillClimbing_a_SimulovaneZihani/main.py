from Interval import Interval
from Functions import Functions
from SearchAlgorithms import SearchAlgorithms
from Graph import Graph
import numpy as np

functions = Functions()
searchAlgorithms = SearchAlgorithms()

# Nastavenia intervalov jednotlivých funkcií
interval_sphere = Interval(-5.12,  5.12, 0.5)
interval_rosenbrock = Interval(-2.048,  2.048, 0.15)
interval_schwefel = Interval(-500, 500, 30)
interval_rastrigin = Interval(-5.12, 5.12, 0.3)
interval_griewank = Interval(-5, 5, 0.5)
interval_levy = Interval(-10, 10, 1)
interval_michalewicz = Interval(0, np.pi, 0.1)
interval_zakharov = Interval(-10, 10, 1)
interval_ackley = Interval(-32.768, 32.768, 3)

# Nastavenia rychlosti animácie
interval_animation_hill_climbing = 10
interval_animation_simulated_annealing = 1

# Nastavenie počtu opakovaní pre daný algorytmus
cycles_hill_climbing = 100
cycles_simulated_annealing = 20

#Vykreslenie grafov funkcie - samotný graf
def draw_graphs():
    # Vykreslenie funkcie Sphere
    graph = Graph(functions.Sphere, interval_sphere)
    graph.Show("Sphere")

    # Vykreslenie funkcie Rosenbrock
    graph = Graph(functions.Rosenbrock, interval_rosenbrock)
    graph.Show("Rosenbrock")

    # Vykreslenie funkcie Schwefel
    graph = Graph(functions.Schwefel, interval_schwefel)
    graph.Show("Schwefel")

    # Vykreslenie funkcie Rastrigin
    graph = Graph(functions.Rastrigin, interval_rastrigin)
    graph.Show("Rastrigin")

    # Vykreslenie funkcie Griewank
    interval_griewank = Interval(-5, 5, 0.1)
    graph = Graph(functions.Griewank, interval_griewank)
    graph.Show("Griewank")

    # Vykreslenie funkcie Levy
    interval_levy = Interval(-10, 10, 0.2)
    graph = Graph(functions.Levy, interval_levy)
    graph.Show("Levy")

    # Vykreslenie funkcie Michalewicz
    interval_michalewicz = Interval(0, np.pi, 0.1)
    graph = Graph(functions.Michalewicz, interval_michalewicz)
    graph.Show("Michalewicz")

    # Vykreslenie funkcie Zakharov
    graph = Graph(functions.Zakharov, interval_zakharov)
    graph.Show("Zakharov")

    # Vykreslenei funkcie Ackley
    graph = Graph(functions.Ackley, interval_ackley)
    graph.Show("Ackley")

def draw_hill_climbing():
    # Vykreslenie funkcie Sphere + body Hill Climbing algoritmu
    best_result, best_choice = searchAlgorithms.HillClimbing(cycles_hill_climbing, 2, interval_sphere, functions.Sphere, "Sphere", interval_animation_hill_climbing)
    print("Najlepšia hodnota je", best_result, "s výberom ", best_choice[0], " a ", best_choice[1])

    # Vykreslenie funkcie Rosenbrock + body z Hill Climbing algoritmu
    best_result, best_choice = searchAlgorithms.HillClimbing(cycles_hill_climbing, 2, interval_rosenbrock, functions.Rosenbrock, "Rosenbrock", interval_animation_hill_climbing)
    print("Najlepšia hodnota je", best_result, "s výberom ", best_choice[0], " a ", best_choice[1])

    # Vykreslenie funkcie Schwefel + body z Hill Climbing algoritmu
    best_result, best_choice = searchAlgorithms.HillClimbing(cycles_hill_climbing, 2, interval_schwefel, functions.Schwefel, "Schwefel", interval_animation_hill_climbing)
    print("Najlepšia hodnota je", best_result, "s výberom ", best_choice[0], " a ", best_choice[1])

    # Vykreslenie funkcie Rastrigin + body z Hill Climbing algoritmu
    best_result, best_choice = searchAlgorithms.HillClimbing(cycles_hill_climbing, 2, interval_rastrigin, functions.Rastrigin, "Rastrigin", interval_animation_hill_climbing)
    print("Najlepšia hodnota je", best_result, "s výberom ", best_choice[0], " a ", best_choice[1])

    # Vykreslenie funkcie Griewank + body z Hill Climbing algoritmu
    best_result, best_choice = searchAlgorithms.HillClimbing(cycles_hill_climbing, 2, interval_griewank, functions.Griewank, "Griewank", interval_animation_hill_climbing)
    print("Najlepšia hodnota je", best_result, "s výberom ", best_choice[0], " a ", best_choice[1])

    # Vykreslenie funkcie Levy + body z Hill Climbing algoritmu
    best_result, best_choice = searchAlgorithms.HillClimbing(cycles_hill_climbing, 2, interval_levy, functions.Levy, "Levy", interval_animation_hill_climbing)
    print("Najlepšia hodnota je", best_result, "s výberom ", best_choice[0], " a ", best_choice[1])

    # Vykreslenie funkcie Michalewicz + body z Hill Climbing algoritmu
    best_result, best_choice = searchAlgorithms.HillClimbing(cycles_hill_climbing, 2, interval_michalewicz, functions.Michalewicz, "Michalewicz", interval_animation_hill_climbing)
    print("Najlepšia hodnota je", best_result, "s výberom ", best_choice[0], " a ", best_choice[1])

    # Vykreslenie funkcie Zakharov + body z Hill Climbing algoritmu
    best_result, best_choice = searchAlgorithms.HillClimbing(cycles_hill_climbing, 2, interval_zakharov, functions.Zakharov, "Zakharov", interval_animation_hill_climbing)
    print("Najlepšia hodnota je", best_result, "s výberom ", best_choice[0], " a ", best_choice[1])

    # Vykreslenie funkcie Ackley + body z Hill Climbing algoritmu
    best_result, best_choice = searchAlgorithms.HillClimbing(cycles_hill_climbing, 2, interval_ackley, functions.Ackley, "Ackley", interval_animation_hill_climbing)
    print("Najlepšia hodnota je", best_result, "s výberom ", best_choice[0], " a ", best_choice[1])

def draw_simulated_annealing():
    # Vykreslenie funkcie Sphere + body z Simulated Annealing algoritmu
    best_result, best_choice = searchAlgorithms.SimulatedAnnealing(cycles_simulated_annealing, 2, interval_sphere, functions.Sphere, "Sphere", interval_animation_simulated_annealing)
    print("Najlepšia hodnota je", best_result, "s výberom ", best_choice[0], " a ", best_choice[1])

    # Vykreslenie funkcie Rosenbrock + body z Simulated Annealing algoritmu
    best_result, best_choice = searchAlgorithms.SimulatedAnnealing(cycles_simulated_annealing, 2, interval_rosenbrock, functions.Rosenbrock, "Rosenbrock", interval_animation_simulated_annealing)
    print("Najlepšia hodnota je", best_result, "s výberom ", best_choice[0], " a ", best_choice[1])

    # Vykreslenie funkcie Schwefel + body z Simulated Annealing algoritmu
    best_result, best_choice = searchAlgorithms.SimulatedAnnealing(cycles_simulated_annealing, 2, interval_schwefel, functions.Schwefel, "Schwefel", interval_animation_simulated_annealing)
    print("Najlepšia hodnota je", best_result, "s výberom ", best_choice[0], " a ", best_choice[1])

    # Vykreslenie funkcie Rastrigin + body z Simulated Annealing algoritmu
    best_result, best_choice = searchAlgorithms.SimulatedAnnealing(cycles_simulated_annealing, 2, interval_rastrigin, functions.Rastrigin, "Rastrigin", interval_animation_simulated_annealing)
    print("Najlepšia hodnota je", best_result, "s výberom ", best_choice[0], " a ", best_choice[1])

    # Vykreslenie funkcie Griewank + body z Simulated Annealing algoritmu
    best_result, best_choice = searchAlgorithms.SimulatedAnnealing(cycles_simulated_annealing, 2, interval_griewank, functions.Griewank, "Griewank", interval_animation_simulated_annealing)
    print("Najlepšia hodnota je", best_result, "s výberom ", best_choice[0], " a ", best_choice[1])

    # Vykreslenie funkcie Levy + body z z Simulated Annealing algoritmu
    best_result, best_choice = searchAlgorithms.SimulatedAnnealing(cycles_simulated_annealing, 2, interval_levy, functions.Levy, "Levy", interval_animation_simulated_annealing)
    print("Najlepšia hodnota je", best_result, "s výberom ", best_choice[0], " a ", best_choice[1])

    # Vykreslenie funkcie Michalewicz + body z z Simulated Annealing algoritmu
    best_result, best_choice = searchAlgorithms.SimulatedAnnealing(cycles_simulated_annealing, 2, interval_michalewicz, functions.Michalewicz, "Michalewicz", interval_animation_simulated_annealing)
    print("Najlepšia hodnota je", best_result, "s výberom ", best_choice[0], " a ", best_choice[1])

    # Vykreslenie funkcie Zakharov + body z z Simulated Annealing algoritmu
    best_result, best_choice = searchAlgorithms.SimulatedAnnealing(cycles_simulated_annealing, 2, interval_zakharov, functions.Zakharov, "Zakharov", interval_animation_simulated_annealing)
    print("Najlepšia hodnota je", best_result, "s výberom ", best_choice[0], " a ", best_choice[1])

    # Vykreslenie funkcie Ackley + body z z Simulated Annealing algoritmu
    best_result, best_choice = searchAlgorithms.SimulatedAnnealing(cycles_simulated_annealing, 2, interval_ackley, functions.Ackley, "Ackley", interval_animation_simulated_annealing)
    print("Najlepšia hodnota je", best_result, "s výberom ", best_choice[0], " a ", best_choice[1])


#odkomentovať podľa toho čo treba spustiť
#draw_graphs()
draw_hill_climbing()
#draw_simulated_annealing()