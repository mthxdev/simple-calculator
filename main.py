import tkinter as tk
from tkinter import messagebox
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
def effectuer_operation(operation):
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        resultat = getattr(calc, operation)(a, b)
        label_resultat.config(text=f"Résultat: {resultat}")
    except ValueError as ve:
        messagebox.showerror("Erreur", str(ve))
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue: {e}")
calc = Calculatrice()

fenetre = tk.Tk()
fenetre.title("Calculatrice Simple")
fenetre.geometry("225x125")

tk.Label(fenetre, text="Nombre A:").grid(row=0, column=0)
entry_a = tk.Entry(fenetre)
entry_a.grid(row=0, column=1)

tk.Label(fenetre, text="Nombre B:").grid(row=1, column=0)
entry_b = tk.Entry(fenetre)
entry_b.grid(row=1, column=1)

btn_add = tk.Button(fenetre, text="Addition", command=lambda: effectuer_operation('addition'))
btn_add.grid(row=2, column=0)

btn_sub = tk.Button(fenetre, text="Soustraction", command=lambda: effectuer_operation('soustraction'))
btn_sub.grid(row=2, column=1)

btn_mul = tk.Button(fenetre, text="Multiplication", command=lambda: effectuer_operation('multiplication'))
btn_mul.grid(row=3, column=0)

btn_div = tk.Button(fenetre, text="Division", command=lambda: effectuer_operation('division'))
btn_div.grid(row=3, column=1)

label_resultat = tk.Label(fenetre, text="Résultat:")
label_resultat.grid(row=4, columnspan=2)

fenetre.mainloop()