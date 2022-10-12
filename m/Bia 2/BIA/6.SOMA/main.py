from Interval import Interval
from Functions import Functions
from SearchAlgorithms import SearchAlgorithms
from Graph import Graph
import numpy as np

functions = Functions()
searchAlgorithms = SearchAlgorithms()

def draw_graphs():
    # Vykreslenie funkcie Sphere
    interval_sphere = Interval(-5.12,  5.12, 0.1)
    graph = Graph(functions.Sphere, interval_sphere)
    graph.Show("Sphere")

    # Vykreslenie funkcee Rosenbrock
    interval_rosenbrock = Interval(-2.048,  2.048, 0.03)
    graph = Graph(functions.Rosenbrock, interval_rosenbrock)
    graph.Show("Rosenbrock")

    # Vykreslenie funkcee Schwefel
    interval_schwefel = Interval(-500, 500, 10)
    graph = Graph(functions.Schwefel, interval_schwefel)
    graph.Show("Schwefel")

    # Vykreslenie funkcee Rastrigin
    interval_rastrigin = Interval(-5.12, 5.12, 0.1)
    graph = Graph(functions.Rastrigin, interval_rastrigin)
    graph.Show("Rastrigin")

    # Vykreslenie funkcee Griewank
    interval_griewank = Interval(-5, 5, 0.1)
    graph = Graph(functions.Griewank, interval_griewank)
    graph.Show("Griewank")

    # Vykreslenie funkcee Levy
    interval_levy = Interval(-10, 10, 0.2)
    graph = Graph(functions.Levy, interval_levy)
    graph.Show("Levy")

    # Vykreslenie funkcee Michalewicz
    interval_michalewicz = Interval(0, np.pi, 0.1)
    graph = Graph(functions.Michalewicz, interval_michalewicz)
    graph.Show("Michalewicz")

    # Vykreslenie funkcee Zakharov
    interval_zakharov = Interval(-10, 10, 0.2)
    graph = Graph(functions.Zakharov, interval_zakharov)
    graph.Show("Zakharov")

    # Vykreslenie funkcie Ackley
    interval_ackley = Interval(-32.768, 32.768, 2)
    graph = Graph(functions.Ackley, interval_ackley)
    graph.Show("Ackley")

def draw_self_organizing_migration():
    # Vykreslenie funkcee Sphere vrátane bodov z Self Organizing Migration algoritmu
    searchAlgorithms.SelfOrganizingMigration(2, interval_sphere, functions.Sphere, "Sphere", interval_animation_self_organizing_migration)

    # Vykreslenie funkcie Rosenbrock vrátane bodov z Self Organizing Migration algoritmu
    searchAlgorithms.SelfOrganizingMigration(2, interval_rosenbrock, functions.Rosenbrock, "Rosenbrock", interval_animation_self_organizing_migration)

    # Vykreslenie funkcie Schwefel vrátane bodov z Self Organizing Migration algoritmu
    searchAlgorithms.SelfOrganizingMigration(2, interval_schwefel, functions.Schwefel, "Schwefel", interval_animation_self_organizing_migration)

    # Vykreslenie funkcie Rastrigin vrátane bodov z Self Organizing Migration algoritmu
    searchAlgorithms.SelfOrganizingMigration(2, interval_rastrigin, functions.Rastrigin, "Rastrigin", interval_animation_self_organizing_migration)

    # Vykreslenie funkcie Griewank vrátane bodov z Self Organizing Migration algoritmu
    searchAlgorithms.SelfOrganizingMigration(2, interval_griewank, functions.Griewank, "Griewank", interval_animation_self_organizing_migration)

    # Vykreslenie funkcie Levy vrátane bodov z Self Organizing Migration algoritmu
    searchAlgorithms.SelfOrganizingMigration(2, interval_levy, functions.Levy, "Levy", interval_animation_self_organizing_migration)

    # Vykreslenie funkcie Michalewicz vrátane bodov z Self Organizing Migration algoritmu
    searchAlgorithms.SelfOrganizingMigration(2, interval_michalewicz, functions.Michalewicz, "Michalewicz", interval_animation_self_organizing_migration)

    # Vykreslenie funkcie Zakharov vrátane bodov z Self Organizing Migration algoritmu
    searchAlgorithms.SelfOrganizingMigration(2, interval_zakharov, functions.Zakharov, "Zakharov", interval_animation_self_organizing_migration)

    # Vykreslenie funkcie Ackley vrátane bodov z Self Organizing Migration algoritmu
    searchAlgorithms.SelfOrganizingMigration(2, interval_ackley, functions.Ackley, "Ackley", interval_animation_self_organizing_migration)

# Nastavenie intervalov jednotlivých funkcií
interval_sphere = Interval(-5.12,  5.12, 0.5)
interval_rosenbrock = Interval(-2.048,  2.048, 0.15)
interval_schwefel = Interval(-500, 500, 30)
interval_rastrigin = Interval(-5.12, 5.12, 0.3)
interval_griewank = Interval(-5, 5, 0.5)
interval_levy = Interval(-10, 10, 1)
interval_michalewicz = Interval(0, np.pi, 0.1)
interval_zakharov = Interval(-10, 10, 1)
interval_ackley = Interval(-32.768, 32.768, 3)

# Nastavenie rychlosti animacie
interval_animation_self_organizing_migration = 1000

# Vykreslenie algoritmu
draw_self_organizing_migration()