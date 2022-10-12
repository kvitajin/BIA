import copy

class Individual:

    def __init__(self, coordinates, index):
        self.coordinates = coordinates
        self.f = None
        self.new_position = [0] * len(self.coordinates)
        self.new_position_f = None
        self.index = index  # označuje jedinečnost jedinca

    # Urobí výpočet na konkrétnej funkcii
    def CalculateF(self, func):
        self.f = func(self.coordinates)

    # Výpočet novej pozicie jedinca, samotná funkcia kontroluje hranice na základe získaného rozsahu intervalu
    def CalculateNewPosition(self, t, PRTVector, individual_best, interval):
        position = []
        length = len(self.new_position)
        for i in range(length):
            position.append(self.coordinates[i] + (individual_best.coordinates[i] - self.coordinates[i]) * t * PRTVector)
            if position[i] < interval.lowerBound:
                position[i] = interval.lowerBound
            elif position[i] > interval.upperBound:
                position[i] = interval.upperBound

        return position

    #  Vypočíta nové pozicie na konkrétnej funkcii
    def CalculateNewPositionF(self, func, position):
        return func(position)

    # Uloží novu najdenu poziciu ako aktuálnu
    def SavePosition(self):
        if self.new_position_f <= self.f:
            self.coordinates = copy.deepcopy(self.new_position)
            self.f = self.new_position_f

    # Vygeneruje novu poziciu, ktorá je v aktuálnom mieste (ešte nedošlo k požiadavkam o pohyb)
    def GenerateNewPosition(self):
        self.new_position = copy.deepcopy(self.coordinates)
        self.new_position_f = self.f