"""
Scientific Calculator App
--------------------------
A calculator built with Tkinter that supports:
- Basic arithmetic operations (+, -, *, /)
- Parentheses
- Powers (^)
- Square root (√)
- Trigonometric functions (sin, cos, tan)
- Logarithmic functions (log, ln)
- Exponential (exp), absolute value (abs), factorial (!)
- Constants (π, e)
"""

import tkinter as tk
import math

# --- Theme Constants ---
BG_COLOR = "#1e1e1e"       # Background color for the window
BTN_COLOR = "#333333"      # Button background color
TEXT_COLOR = "#ffffff"     # Text color (buttons and entry)
FONT = ("Helvetica", 18)   # Font for buttons and entry

# ==========================
# Functional Logic Handlers
# ==========================

def on_click(value):
    """
    Handles button clicks. Adds the corresponding symbol or function
    to the entry field depending on the button pressed.
    """
    if value == 'π':
        entry.insert(tk.END, str(math.pi))
    elif value == 'e':
        entry.insert(tk.END, str(math.e))
    elif value in ['sin', 'cos', 'tan', 'log', 'ln', 'sqrt', 'exp', 'abs']:
        # Insert as a function call, e.g., sin(
        entry.insert(tk.END, f"{value}(")
    elif value == '^':
        # Translate caret to Python exponentiation syntax
        entry.insert(tk.END, '**')
    elif value == '!':
        # Insert Python factorial function call
        entry.insert(tk.END, 'math.factorial(')
    else:
        # Default: insert the symbol or number as-is
        entry.insert(tk.END, str(value))

def clear_entry():
    """
    Clears the entire input field.
    """
    entry.delete(0, tk.END)

def delete_last():
    """
    Deletes the last character from the entry field.
    """
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(tk.END, current[:-1])

def calculate():
    """
    Evaluates the expression written in the entry field.
    Replaces function names with corresponding Python math functions.
    Handles invalid inputs with error display.
    """
    try:
        expr = entry.get()
        # Map UI functions to math module equivalents
        expr = expr.replace('ln', 'math.log')
        expr = expr.replace('log', 'math.log10')
        expr = expr.replace('sin', 'math.sin')
        expr = expr.replace('cos', 'math.cos')
        expr = expr.replace('tan', 'math.tan')
        expr = expr.replace('sqrt', 'math.sqrt')
        expr = expr.replace('exp', 'math.exp')
        expr = expr.replace('abs', 'abs')
        expr = expr.replace('π', str(math.pi))
        expr = expr.replace('e', str(math.e))

        result = eval(expr)  # <!> Trusted context only
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

# ==========================
# GUI Initialization
# ==========================

# Create main application window
root = tk.Tk()
root.title("Scientific Calculator")
root.geometry("400x550")
root.configure(bg=BG_COLOR)

# Make grid responsive
for i in range(7):  # Total rows
    root.grid_rowconfigure(i, weight=1)
for i in range(4):  # Total columns
    root.grid_columnconfigure(i, weight=1)

# ==========================
# Entry Field (Display)
# ==========================
entry = tk.Entry(
    root,
    font=("Helvetica", 24),
    bd=0,
    bg=BTN_COLOR,
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,  # Cursor color
    justify='right'
)
entry.grid(row=0, column=0, columnspan=4, sticky='nsew', padx=10, pady=10)

# ==========================
# Button Configuration
# ==========================
buttons = [
    # Row 1
    ('7',1,0), ('8',1,1), ('9',1,2), ('+',1,3),
    # Row 2
    ('4',2,0), ('5',2,1), ('6',2,2), ('-',2,3),
    # Row 3
    ('1',3,0), ('2',3,1), ('3',3,2), ('*',3,3),
    # Row 4
    ('0',4,0), ('.',4,1), ('=',4,2), ('/',4,3),
    # Row 5
    ('(',5,0), (')',5,1), ('C',5,2), ('<-',5,3),
    # Row 6
    ('π',6,0), ('e',6,1), ('^',6,2), ('√',6,3),
    # Row 7
    ('sin',7,0), ('cos',7,1), ('tan',7,2), ('log',7,3),
    # Row 8
    ('ln',8,0), ('exp',8,1), ('abs',8,2), ('!',8,3)
]

# Create and place each button
for (text, row, col) in buttons:
    # Determine the button's action
    if text == '=':
        action = calculate
    elif text == 'C':
        action = clear_entry
    elif text == '<-':
        action = delete_last
    elif text == '√':
        # Special case for square root shortcut
        action = lambda x='sqrt': on_click(x)
    else:
        action = lambda x=text: on_click(x)

    # Create button widget
    btn = tk.Button(
        root,
        text=text,
        font=FONT,
        command=action,
        bg=BTN_COLOR,
        fg=TEXT_COLOR,
        bd=0,
        activebackground="#555555",
        activeforeground="#ffffff"
    )
    btn.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)

# ==========================
# Start the Application Loop
# ==========================
root.mainloop()
