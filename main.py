import tkinter as tk

def on_click(value):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(tk.END, current + str(value))

def clear_entry():
    entry.delete(0, tk.END)

def delete_last():
    current = entry.get()
    current_new = current[:-1]
    entry.delete(0, tk.END)
    entry.insert(tk.END, current_new)

def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0,tk.END)
        entry.insert(0, str(result))
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")
root = tk.Tk()
root.title("Simple Calculator")
root.geometry("320x415")

entry = tk.Entry(root, width=16, font=("Arial", 24), bd=5, relief=tk.SUNKEN, justify='right')
entry.grid(row=0, column=0, columnspan=4)

buttons = [
    ('7',1,0), ('8',1,1), ('9',1,2), ('+',1,3),
    ('4',2,0), ('5',2,1), ('6',2,2), ('-',2,3),
    ('1',3,0), ('2',3,1), ('3',3,2), ('*',3,3),
    ('0',4,0), ('.',4,1), ('=',4,2), ('/',4,3),
    ('C',5,0,2), ('<-',5,2,2)
]

for (text, row, col, colspan) in [(b[0], b[1], b[2], 1) if len(b) == 3 else b for b in buttons]:
    if text == '=':
        action = calculate
    elif text == 'C':
        action = clear_entry
    elif text == '<-':
        action = delete_last
    else:
        action = lambda x=text: on_click(x)
    
    tk.Button(root, text=text, width=5, height=2, font=("Arial", 18), command=action)\
        .grid(row=row, column=col, columnspan=colspan, sticky='nsew')


root.mainloop()