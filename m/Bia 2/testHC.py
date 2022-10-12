import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import random
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3

#TODO:
    #cv1_1.py blindSearch

class Solution:
    def __init__(self, dimension, lower_bound, upper_bound):
        self.dimension = dimension
        self.lB = lower_bound
        self.uB = upper_bound
        self.parameters = np.zeros(self.dimension) #Return a new array of given shape and type, filled with zeros
        self.f = np.inf #constants IEEE 754 floating point representation of (positive) infinity.



    def hillClimbing(self, numberOfGenerations, numberOfPoints, sigma, function):
        fullResultsArray = []
        npArray = []
        self.parameters = np.zeros(self.dimension)
        for i in range(0, self.dimension):
            generatedValue = random.uniform(self.lB,self.uB)
            self.parameters[i] = generatedValue

        initValue = function(self.parameters)
        npArray = np.append(self.parameters, [initValue])
        fullResultsArray.append(npArray)
        
        for i in range(numberOfGenerations):
            neighbors = [] 
            for j in range(numberOfPoints):    
                generatedNeighbor = np.random.normal(self.parameters,sigma)
                neighbor = function(generatedNeighbor)
                
                if initValue >= neighbor :
                    self.parameters = generatedNeighbor
                    initValue = neighbor
                    npArray = np.append(self.parameters,[neighbor])
            fullResultsArray.append(npArray)
        print(fullResultsArray)
     
        

class Function:
    def __init__(self, name):
        self.name = name

    def sphere(self, params):
        sum = 0
        for p in params:
            sum += p ** 2
        return sum

    def schwefel(self, params):
        sum = 0
        for i in range(params):
            sum += params[i] * np.sin(np.sqrt(np.abs(params[i])))
        
        return 418.9829 * len(params) - sum

    def rosenbrock(self, params):
        sum = 0
        for i in range(len(params) - 1):
            sum += 100 * (params[i + 1] - params[i] ** 2) ** 2 + (params[i] - 1) ** 2
        return sum

    def rastrigin(self, params):
        sum = 0
        d = len(params)
        for x in params:
            sum += ((x ** 2) - 10 * np.cos(2 * np.pi * x))
        return (10 * d) + sum
    
    
    def griewangk(self, params):
        sum = 0
        multiply = 1
        for i in range(len(params)):
            sum += (params[i] ** 2) / 4000
        for i in range(len(params)):
            multiply *= np.cos( params[i] / np.sqrt(i + 1))
        
        return sum - multiply + 1

    def levy(self, params):
        sum = 0
        Wd = params[len(params)-1]

        for i in range(len(params) - 1):
            Wi = 1 + (params[i] - 1) / 4
            sum += ((Wi - 2) ** 2) * (1+10 * np.sin(np.pi * Wi + 1) **2 ) + ((Wd - 1) ** 2) * (1 + np.sin(2 * np.pi * Wd)**2)
        return np.sin(np.pi * params[0]) ** 2 + sum 

    def michalewicz(self, params):
        sum = 0
        m = 10
        for i in range(len(params)):
            sum += np.sin(params[i])*(np.sin(((i + 1)*(params[i] ** 2)) / np.pi)) ** (2 * m)
        return -sum

    def Zakharov(self, params):
        sum1 = 0
        sum2 = 0
        sum3 = 0
        for i in range(len(params)):
            sum1 += params[i] ** 2
            sum2 += (0.5 * (i) * params[i]) ** 2
            sum3 += (0.5 * (i) * params[i]) ** 4
        return sum1 + sum2 + sum3

    def Ackley(self, params):
        sum1 = 0
        sum2 = 0
        a = 20
        b = 0.2
        c = 2 * np.pi
        d = len(params)

        for x in params:
            sum1 += x ** 2
            sum2 += np.cos(c * x)
        return -a * np.exp(-b * np.sqrt(sum1 / d)) - np.exp(sum2 / d) + a + np.exp(1)

solution = Solution(2, -5.12, 5.12)
function = Function("My Functions")
solution.hillClimbing(5, 5, 0.33 ,function.sphere)
