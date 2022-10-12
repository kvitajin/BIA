from Interval import Interval
from Functions import Functions
from SearchAlgorithms import SearchAlgorithms
from Graph import Graph
import numpy as np

functions = Functions()
searchAlgorithms = SearchAlgorithms()

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

def draw_particle_swarm():
    # Vykreslenie funkcie Sphere vrátane bodov z Particle Swarm algoritmu
    searchAlgorithms.ParticleSwarm(2, interval_sphere, functions.Sphere, "Sphere", interval_animation_particle_swarm)

    # Vykreslenie funkcie Rosenbrock vrátane bodov z Particle Swarm algoritmu
    searchAlgorithms.ParticleSwarm(2, interval_rosenbrock, functions.Rosenbrock, "Rosenbrock", interval_animation_particle_swarm)

    # Vykreslenie funkcie Schwefel vrátane bodov z Particle Swarm algoritmu
    searchAlgorithms.ParticleSwarm(2, interval_schwefel, functions.Schwefel, "Schwefel", interval_animation_particle_swarm)

    # Vykreslenie funkcie Rastrigin vrátane bodov z Particle Swarm algoritmu
    searchAlgorithms.ParticleSwarm(2, interval_rastrigin, functions.Rastrigin, "Rastrigin", interval_animation_particle_swarm)

    # Vykreslenie funkcie Griewank vrátane bodov z Particle Swarm algoritmu
    searchAlgorithms.ParticleSwarm(2, interval_griewank, functions.Griewank, "Griewank", interval_animation_particle_swarm)

    # Vykreslenie funkcie Levy vrátane bodov z Particle Swarm algoritmu
    searchAlgorithms.ParticleSwarm(2, interval_levy, functions.Levy, "Levy", interval_animation_particle_swarm)

    # Vykreslenie funkcie Michalewicz vrátane bodov z Particle Swarm algoritmu
    searchAlgorithms.ParticleSwarm(2, interval_michalewicz, functions.Michalewicz, "Michalewicz", interval_animation_particle_swarm)

    # Vykreslenie funkcie Zakharov vrátane bodov z Particle Swarm algoritmu
    searchAlgorithms.ParticleSwarm(2, interval_zakharov, functions.Zakharov, "Zakharov", interval_animation_particle_swarm)

    # Vykreslenie funkcie Ackley vrátane bodov z Particle Swarm algoritmu
    searchAlgorithms.ParticleSwarm(2, interval_ackley, functions.Ackley, "Ackley", interval_animation_particle_swarm)

# Nastavenie intervalu jednotlivých funkcií
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
interval_animation_particle_swarm = 1

# Vykreslenie všetkých funkcií podľa zvoleného algorytmu
draw_particle_swarm()