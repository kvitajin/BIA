from mpl_toolkits import mplot3d
import math
import random
import matplotlib.pyplot as plt 
from matplotlib import cm
import numpy as np


class Function:
    def __init__(self, name):
        self.name = name

    def Sphere(self, par):
        res = 0
        for x in par:
            res+=x**2
        return res 

    def Schwefel(self, par): 
        sum=0
        for i in range(len(par)):
            sum += par[i]*np.sin(np.sqrt(np.abs(par[i]))); 
        
        return 418.9829*len(par) - sum

    def Ackley(self, par):
        a = 20
        b = 0.2
        c = 2 * math.pi
        sum1 = 0
        sum2 = 0
        for i in range(len(par)):
            sum1 += par[i]**2
            sum2 += np.cos(c * par[i])  
            #vyhadzovalo delenie nulou 
            if(i!=0):    
                res = -a * np.exp(-b*np.sqrt((1/i)*sum1)) - np.exp((1/i)*sum2) + a + np.exp(1)
    
        return res  

    def Rosenbrock(self, par):
        sum=0
        for i in range(0, len(par)-1):
            sum+=(100*(par[i+1] - par[i]**2)**2 + (par[i] - 1)**2)
        return sum

    def Rastrigin(self, par):
        sum=0

        for x in par:
            sum+= x**2 - 10*np.cos(2*np.pi*x)

        z = 10*len(par) + sum
        return z

    def Griewank(self, par):
        sum=0
        prod=0
        for i in range(len(par)):
            sum += (par[i]**2)/4000
            if i!=0:
                prod = prod * np.cos(par[i]/np.sqrt(i))
        return sum - prod + 1

    def Levy(self, par):
        sum= 0
        w_d = 1 + ((par[len(par)-1] - 1) / 4)
        w_1 = 1 + ((par[0] - 1) / 4)

        for i in range(0, len(par)-1):
            w_i = 1 + ((par[i] - 1) / 4)
            sum+= (w_i - 1)**2 * (1 + 10*np.sin(np.pi*w_i+1)**2) + (w_d-1)**2 * (1+np.sin(2*np.pi*w_d)**2) 

        return np.sin(np.pi*w_1)**2 + sum
    
    def Michalewicz(self, par):
        sum= 0
        m=10
        
        for i in range(len(par)):
            sum += np.sin(par[i]) * (np.sin(i*par[i])**2/np.pi)**(2*m)
        return -1 * sum

    def Zakharov(self, par):
        sum1= 0
        sum2=0
        for i in range(len(par)):
            sum1 = sum1 + par[i]**2
            sum2 = sum2 + 0.5*i*par[i]
        return sum1 + sum2**2 + sum2**4    

class Solution:
    def __init__(self, dimension, lower_bound, upper_bound):
        self.dimension = dimension
        self.lB = lower_bound 
        self.uB = upper_bound
        self.parameters = np.zeros(self.dimension) 
        self.f = np.inf  

    #values - body vykreslovane do grafu, ak je prázdne vykreslí sa len graf
    def draw(self, min, max, f, values):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        X = np.linspace(min, max, 200)
        Y = np.linspace(min, max, 200)
        X, Y = np.meshgrid(X, Y)
        Z = f([X, Y])
        ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,alpha=0.7)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        if values.__len__!=0:
            for value in values:
                x=value[0]
                y=value[1]
                z=value[2]
                ax.scatter3D(x, y, z)

        plt.show()    
    
    def hillClimb(self, f, tMax, sigma, nCount):
        temp = [] 
        res = []
              
        for i in range(0, self.dimension):            
            x0 = random.uniform(self.lB,self.uB)
            self.parameters[i] = x0

        bestValue = f(self.parameters)
        temp = np.append(self.parameters, [bestValue])
        res.append(temp)

        print("Start position:")
        print(self.parameters)
        print(bestValue)
        
        for i in range(0, tMax):
            for j in range(0, nCount):    
                n = np.random.normal(self.parameters,sigma)
                #print(n)
                nValue = f(n)
                
                if bestValue >= nValue :
                    print("New best value:")
                    print(nValue)
                    self.parameters = n
                    bestValue = f(self.parameters)
                    temp = np.append(self.parameters,[nValue])
            res.append(temp)
    
        return res       

#ackley -32.768, 32.768        
#sphere -5.12,5.12
#schwefel  -500,500
#rosenbrock  -6,6
#rastrigin  -5.12,5.12
#griewank  -5,5
#levy  -10,10
#michalewicz  0,np.pi
#zakharov -10,10


sphere = Solution(2,-5.12,5.12)
ackley = Solution(2,-32.768, 32.768)
f = Function("")

sphere.draw(sphere.uB,sphere.lB,f.Sphere,sphere.hillClimb(f.Sphere,10,0.5,5))
ackley.draw(ackley.uB,ackley.lB,f.Ackley,ackley.hillClimb(f.Ackley,10,0.2,5))


