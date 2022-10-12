from Interval import Interval
from SearchAlgorithms import SearchAlgorithms
from Graph import Graph
import numpy as np

from Point import Point

searchAlgorithms = SearchAlgorithms()

interval = Interval(0, 200)
searchAlgorithms.AntColony(interval)