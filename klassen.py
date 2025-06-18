import random

class Zahlen:
    def __init__(self):
        self.zahl1 = 0
        self.zahl2 = 0
        self.ergebnis_plus = None
        self.ergebnis_minus = None

    def result(self):
        self.ergebnis_plus = self.zahl1 + self.zahl2
        self.ergebnis_minus = self.zahl1 - self.zahl2

    def generieren(self, wert):
        def einfach(self):
            self.zahl2 = random.randint(10, 100)
            self.zahl1 = random.randint(self.zahl2, 100)

        def normal(self):
            self.zahl1 = random.randint(10, 100)
            self.zahl2 = random.randint(10, 100)
        
        def schwer(self):
            self.zahl1 = random.randint(10, 1000)
            self.zahl2 = random.randint(10, 1000)

        if wert == "Leicht":
            einfach(self)
        elif wert == "Mittel":
            normal(self)
        elif wert == "Schwer":
            schwer(self)
        else:
            print("Fehler")


class Nutzer:
    def __init__(self):
        self.name = None
        self.runden = 0
        self.punkte = 0
        self.fehler = 0