"""
Scientific Calculator (safe evaluator)
-------------------------------------
Tkinter calculator that supports basic arithmetic, parentheses,
power (^), square root (√), trig/log/exp functions and constants (pi, e),
but DOES NOT use eval() on raw input. Uses ast to parse and a whitelist
to evaluate only allowed operations and functions.
"""

import tkinter as tk
import math
import ast
import operator as op

# --- Theme constants ---
BG_COLOR = "#1e1e1e"
BTN_COLOR = "#333333"
TEXT_COLOR = "#ffffff"
FONT = ("Helvetica", 18)

# --- Safety: allowed operators and functions ---
# Map AST operator nodes to Python functions
ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,     # unary minus (e.g. -3)
    ast.UAdd: op.pos      # unary plus (e.g. +3)
}

# Whitelisted functions/constants available to users
ALLOWED_NAMES = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'log': math.log10,   # log -> base 10
    'ln': math.log,      # ln -> natural log
    'sqrt': math.sqrt,
    'exp': math.exp,
    'abs': abs,
    'pi': math.pi,
    'e': math.e,
    'factorial': math.factorial
}

# Global flag to mark that last evaluation produced an error
error_state = False

# =========================
# Safe AST evaluator
# =========================
def safe_eval(node):
    """
    Recursively evaluate an AST node while permitting only:
    - numbers (ast.Constant)
    - binary operations with allowed operators
    - unary operations (negation)
    - function calls where the function name is whitelisted
    - names that are whitelisted constants (pi, e)
    Raises ValueError on any disallowed node.
    """
    # Numbers (Python 3.8+ uses ast.Constant)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        else:
            raise ValueError("Invalid constant")
    # For older ASTs, ast.Num (kept for compatibility)
    if isinstance(node, ast.Num):
        return node.n

    # Binary operations: a <op> b
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type in ALLOWED_OPERATORS:
            left = safe_eval(node.left)
            right = safe_eval(node.right)
            return ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError("Operator not allowed")

    # Unary operations: -a or +a
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type in ALLOWED_OPERATORS:
            operand = safe_eval(node.operand)
            return ALLOWED_OPERATORS[op_type](operand)
        raise ValueError("Unary operator not allowed")

    # Function calls: f(arg1, arg2, ...)
    if isinstance(node, ast.Call):
        # Only allow simple name calls (no attribute access)
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in ALLOWED_NAMES and callable(ALLOWED_NAMES[func_name]):
                args = [safe_eval(arg) for arg in node.args]
                return ALLOWED_NAMES[func_name](*args)
        raise ValueError("Function not allowed")

    # Names/constants (pi, e, etc.)
    if isinstance(node, ast.Name):
        if node.id in ALLOWED_NAMES:
            value = ALLOWED_NAMES[node.id]
            # If it's a function, return function object (should be called)
            if callable(value):
                return value
            return value

    # Anything else is disallowed
    raise ValueError("Invalid expression element")

# =========================
# GUI logic
# =========================
def on_click(value):
    """
    Handle button click insertions. If we are in an error state and the next
    click is a regular input (digit, operator, function), clear first.
    """
    global error_state

    # If last action produced an error, any normal input clears it first
    if error_state:
        # keep special controls (C, <-, =) unaffected
        if value not in ('C', '<-', '='):
            entry.delete(0, tk.END)
            error_state = False

    # Map button labels to entry text
    if value == 'π':
        entry.insert(tk.END, 'pi')
    elif value == 'e':
        entry.insert(tk.END, 'e')
    elif value in ('sin', 'cos', 'tan', 'log', 'ln', 'sqrt', 'exp', 'abs'):
        # Insert function name with opening parenthesis for convenience
        entry.insert(tk.END, f"{value}(")
    elif value == '^':
        entry.insert(tk.END, '**')   # caret -> python power
    elif value == '!':
        # factorial: insert as function call
        entry.insert(tk.END, 'factorial(')
    elif value == '%':
        # percentage: convert x% to (x/100)
        entry.insert(tk.END, '/100')
    else:
        entry.insert(tk.END, str(value))

def clear_entry():
    """Clear the entire display."""
    global error_state
    entry.delete(0, tk.END)
    error_state = False

def delete_last():
    """Delete the last character from the display."""
    current = entry.get()
    if current:
        entry.delete(0, tk.END)
        entry.insert(tk.END, current[:-1])

def calculate():
    """
    Parse and safely evaluate the expression from the entry widget.
    Uses ast.parse and safe_eval to avoid eval().
    Sets an error_state flag when evaluation fails.
    """
    global error_state
    expr = entry.get()

    # Quick textual normalizations from UI symbols to parser-friendly tokens
    expr = expr.replace('π', 'pi').replace('^', '**').replace('√', 'sqrt')

    try:
        # Parse expression into AST (mode='eval' allows only expressions)
        parsed = ast.parse(expr, mode='eval').body
        result = safe_eval(parsed)

        # If result is a float that looks like an integer, show integer
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        entry.delete(0, tk.END)
        entry.insert(0, str(result))
        error_state = False
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")
        error_state = True

# =========================
# GUI initialization
# =========================
root = tk.Tk()
root.title("Scientific Calculator (Safe)")
root.geometry("420x560")
root.configure(bg=BG_COLOR)

# Make rows/columns expandable (responsive layout)
for i in range(9):      # allow for enough rows
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

# Display entry
entry = tk.Entry(
    root,
    font=("Helvetica", 24),
    bd=0,
    bg=BTN_COLOR,
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,
    justify='right'
)
entry.grid(row=0, column=0, columnspan=4, sticky='nsew', padx=10, pady=10)

# Button definitions (label, row, column)
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

# Create buttons and place them in the grid
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

# Start the GUI loop
root.mainloop()
