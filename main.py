import tkinter as tk
import math

BG_COLOR = "#1e1e1e"
BTN_COLOR = "#333333"
TEXT_COLOR = "#ffffff"
FONT = ("Helvetica", 18)

def on_click(value):
    if value == 'π':
        entry.insert(tk.END, str(math.pi))
    elif value == 'e':
        entry.insert(tk.END, str(math.e))
    elif value in ['sin', 'cos', 'tan', 'log', 'ln', 'sqrt', 'exp', 'abs']:
        entry.insert(tk.END, f"{value}(")
    elif value == '^':
        entry.insert(tk.END, '**')
    elif value == '!':
        entry.insert(tk.END, 'math.factorial(')
    else:
        entry.insert(tk.END, str(value))

def clear_entry():
    entry.delete(0, tk.END)

def delete_last():
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(tk.END, current[:-1])

def calculate():
    try:
        expr = entry.get()
        expr = expr.replace('ln', 'math.log')  # ln -> log base e
        expr = expr.replace('log', 'math.log10')
        expr = expr.replace('sin', 'math.sin')
        expr = expr.replace('cos', 'math.cos')
        expr = expr.replace('tan', 'math.tan')
        expr = expr.replace('sqrt', 'math.sqrt')
        expr = expr.replace('exp', 'math.exp')
        expr = expr.replace('abs', 'abs')
        expr = expr.replace('π', str(math.pi))
        expr = expr.replace('e', str(math.e))

        result = eval(expr)
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

root = tk.Tk()
root.title("Scientific Calculator")
root.geometry("400x550")
root.configure(bg=BG_COLOR)

for i in range(7):
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

entry = tk.Entry(root, font=("Helvetica", 24), bd=0, bg=BTN_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, justify='right')
entry.grid(row=0, column=0, columnspan=4, sticky='nsew', padx=10, pady=10)

buttons = [
    ('7',1,0), ('8',1,1), ('9',1,2), ('+',1,3),
    ('4',2,0), ('5',2,1), ('6',2,2), ('-',2,3),
    ('1',3,0), ('2',3,1), ('3',3,2), ('*',3,3),
    ('0',4,0), ('.',4,1), ('=',4,2), ('/',4,3),
    ('(',5,0), (')',5,1), ('C',5,2), ('<-',5,3),
    ('π',6,0), ('e',6,1), ('^',6,2), ('√',6,3),
    ('sin',7,0), ('cos',7,1), ('tan',7,2), ('log',7,3),
    ('ln',8,0), ('exp',8,1), ('abs',8,2), ('!',8,3)
]

for (text, row, col) in buttons:
    if text == '=':
        action = calculate
    elif text == 'C':
        action = clear_entry
    elif text == '<-':
        action = delete_last
    elif text == '√':
        action = lambda x='sqrt': on_click(x)
    else:
        action = lambda x=text: on_click(x)

    btn = tk.Button(root, text=text, font=FONT, command=action,
        bg=BTN_COLOR, fg=TEXT_COLOR, bd=0, activebackground="#555555", activeforeground="#ffffff")
    btn.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)

root.mainloop()
