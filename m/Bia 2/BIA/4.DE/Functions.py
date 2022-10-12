import numpy as np

class Functions:

    def Sphere(self, xx):
        summary = 0
        for x in xx:
            summary += x**2
        return summary

    def Schwefel(self, xx):
        d = len(xx)
        summary = 0
        for x in xx:
            summary += x * np.sin(np.sqrt(np.abs(x)))
        summary = 418.9829 * d - summary
        return summary

    def Rosenbrock(self, xx):
        index = 1
        summary = 0
        for x in xx[:-1]:
            summary += 100 * ((xx[index] - x**2)**2) + (x - 1)**2 
            index += 1
        return summary

    def Rastrigin(self, xx):
        d = len(xx)
        summary = 0
        for x in xx:
            summary += x**2 - 10 * np.cos(2 * np.pi * x)
        summary = d * 200 + summary
        return summary

    def Griewank(self, xx):
        summary = 0
        prod = 1
        i = 1
        for x in xx:
            summary += x**2 / 4000
            prod *= np.cos(x / np.sqrt(i))
            i += 1
        summary = summary - prod + 1
        return summary

    def Levy(self, xx):
        d = len(xx)
        summary = 0
        w = []
        for i in range(len(xx)):
            w.append(1 + (xx[i] - 1) / 4)

        term1 = (np.sin(np.pi * w[1]))**2
        term3 = (w[d-1] - 1)**2 * (1 + (np.sin(2 * np.pi * w[d-1]))**2)

        for wi in w[:-1]:
            summary += (wi - 1)**2 * (1 + 10 * (np.sin(np.pi * wi + 1))**2)
        summary = term1 + summary + term3
        return summary

    def Michalewicz(self, xx):
        summary = 0
        m = 10
        i = 1
        for x in xx:
            summary += np.sin(x) * (np.sin(i * x**2 / np.pi))**(2 * m)
            i += 1
        return -summary

    def Zakharov(self, xx):
        summary1 = 0
        summary2 = 0
        i = 1
        for x in xx:
            summary1 += x**2
            summary2 += 0.5 * i * x
            i += 1
        summary = summary1 + summary2**2 + summary2**4
        return summary

    def Ackley(self, xx):
        d = len(xx)
        summary1 = 0
        summary2 = 0
        a = 20
        b = 0.2
        c = 2 * np.pi
        for x in xx:
            summary1 += x**2
            summary2 += np.cos(c * x)
        summary = (-a * np.exp(-b * np.sqrt(summary1 / d))) + (-np.exp(summary2 / d)) + a + np.exp(1)
        return summary