from Point import Point
import random
import string
import numpy as np

class Cities:

    def __init__(self, interval):
        self.cities = []
        self.distance_matrix = []
        self.visibility_matrix = []
        self.pheromones = None
        self.interval = interval
        # city_index zaručuje jedinečnost v názvu města
        self.city_index = 0

    def Return(self):
        return self.cities

    # Generuje mesto s náhodnou poziciou skrz interval s náhodným jedinečným menom
    def GenerateCity(self):
        city = Point(random.uniform(self.interval.lowerBound, self.interval.upperBound), random.uniform(self.interval.lowerBound, self.interval.upperBound), string.ascii_letters[self.city_index], self.city_index)
        return city

    # Generovánie mest
    def Generate(self, amount):
        if self.cities:
            return

        for _ in range(amount):
            self.cities.append(self.GenerateCity())
            self.city_index += 1

        # Vygenerovanie Distance a Visibility Matrix
        for main_city in self.cities:
            distance = []
            visibility = []
            for city in self.cities:
                if main_city.name == city.name:
                    distance.append(0)
                    visibility.append(0)
                    continue
                city_range = self.CalculateDistance(main_city, city)
                distance.append(city_range)
                visibility.append(1/city_range)

            self.distance_matrix.append(distance)
            self.visibility_matrix.append(visibility)
        
        self.pheromones = np.ones((len(self.cities), len(self.cities)))

    # Výpočet vzdialenosti mezi dvoma mestami
    def CalculateDistance(self, city_from, city_to):
        return np.sqrt((city_from.x - city_to.x)**2 + (city_from.y - city_to.y)**2)