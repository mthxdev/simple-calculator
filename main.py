class Calculatrice:
    def __init__(self):
        self.resultat = 0

    def addition(self, a, b):
        self.resultat = a + b
        return self.resultat

    def soustraction(self, a, b):
        self.resultat = a - b
        return self.resultat

    def multiplication(self, a, b):
        self.resultat = a * b
        return self.resultat

    def division(self, a, b):
        if b > 0 or b < 0:
            self.resultat = a / b
        elif b == 0:
            print("Erreur: Division par zéro")
        return self.resultat
