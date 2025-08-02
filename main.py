class Calculatrice:
    def addition(self, a, b):
        return a + b

    def soustraction(self, a, b):
        return a - b

    def multiplication(self, a, b):
        return a * b
    
    def division(self, a, b):
        if b == 0:
            raise ValueError("Division par zéro n'est pas permise.")
        return a / b
def main():
    calc = Calculatrice()
    
    print("Addition de 5 et 3:", calc.addition(5, 3))
    print("Soustraction de 5 et 3:", calc.soustraction(5, 3))
    print("Multiplication de 5 et 3:", calc.multiplication(5, 3))
    try:
        print("Division de 5 par 0:", calc.division(5, 0))
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()