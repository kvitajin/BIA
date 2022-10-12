import copy

class Individual:

    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.f = None
        self.v = [0] * len(coordinates)
        self.pBest = None
        self.pBestf = None

    # Prevedie výpočet na konkrétnej funkcii
    def CalculateF(self, func):
        self.f = func(self.coordinates)

    # Výpočet vektoru "v" pre smer nového bodu, samotná funkcia kontroluje rychlost na základě získaného rozsahu velocity
    def CalculateV(self, c_1, c_2, r_1, r_2, gBest, velocity, interval):
        length = len(self.v)
        for i in range(length):
            self.v[i] = self.v[i] + r_1 * c_1 * (self.pBest[i] - self.coordinates[i]) + r_2 * c_2 * (gBest.pBest[i] - self.coordinates[i])
            if self.v[i] < velocity[0]:
                self.v[i] = velocity[0]
            elif self.v[i] > velocity[1]:
                self.v[i] = velocity[1]

    # Vygeneruje najlepší nájdený bod
    def GeneratepBest(self):
        if self.pBest is None:
            self.pBest = copy.deepcopy(self.coordinates)
            self.pBestf = self.f