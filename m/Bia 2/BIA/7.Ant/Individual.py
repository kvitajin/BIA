import copy

class Individual:

    def __init__(self, starting_city, max_cities, index):
        self.path = [starting_city]             # Cesta priechodu
        self.starting_city = starting_city      # Startovne mesto
        self.max_cities = max_cities            # Maximálny počet miest
        self.currentDistance = 0                # Aktuálna vzdialenost cesty
        self.index = index                      # Označuje jedinečnost jedince

    # Pridanie mesta do cesty
    def AddCityToPath(self, city):
        if len(self.path) < self.max_cities:
            self.path.append(city)

    # Resetovanie cesty
    def ResetPath(self):
        self.path.clear()
        self.path.append(self.starting_city)

    # Výpočet vzdialenosti mezdi jednotlivými mestami
    def EvaluateDistance(self, func_CalculateDistance):
        path_length = len(self.path)
        evaluation = 0

        # Priechod celej cesty mezdi všetkymi mestamy
        for i in range(path_length):
            # Ak  sa jedná o posledne mesto, vypočítaj poslednú vzdialenost mezi posledním mestom a prvím a pirpočitaj k celku
            if i == path_length - 1:
                evaluation += func_CalculateDistance(self.path[i], self.path[0])
                continue
            # Vypočitaj vzdialenost medzi aktuálnym a následujucim mestem a pripočítaj k celku
            evaluation += func_CalculateDistance(self.path[i], self.path[i + 1])
        
        # Uloženie hodnoty do aktuálnej vzdialenosti (služíi ptm pre výber najlepšieho jedinca)
        self.currentDistance = evaluation
        return evaluation