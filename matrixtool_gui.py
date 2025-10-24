#!/usr/bin/env python3
"""
Matrix Operations Tool (Tkinter GUI)
Paste matrices as:
1 2 3
4 5 6
(each row on its own line; columns separated by space or comma)
"""
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

def parse_matrix_from_text(text):
    lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
    if not lines:
        raise ValueError("No data provided.")
    data = []
    col_count = None
    for i, ln in enumerate(lines, start=1):
        parts = [p for p in ln.replace(',', ' ').split() if p]
        if col_count is None:
            col_count = len(parts)
            if col_count == 0:
                raise ValueError(f"Row {i} is empty.")
        elif len(parts) != col_count:
            raise ValueError(f"Inconsistent number of columns (row {i}). Expected {col_count}.")
        try:
            row = [float(x) for x in parts]
        except ValueError:
            raise ValueError(f"Non-numeric value found on row {i}.")
        data.append(row)
    return np.array(data, dtype=float)

def display_result_matrix(mat, tree, text_widget, label_widget):
    # Clear tree
    for i in tree.get_children():
        tree.delete(i)
    text_widget.delete("1.0", tk.END)
    label_widget.config(text="")

    if mat is None:
        return
    if mat.ndim == 0:
        text_widget.insert(tk.END, str(mat))
        return

    rows, cols = mat.shape
    # configure columns in tree
    tree["columns"] = [f"c{c}" for c in range(cols)]
    tree["show"] = "headings"
    for c in range(cols):
        tree.heading(f"c{c}", text=f"C{c+1}")
        tree.column(f"c{c}", width=80, anchor="e")

    # Insert rows
    for r in range(rows):
        row_values = [format_number(mat[r, c]) for c in range(cols)]
        tree.insert("", "end", values=row_values)

    text_widget.insert(tk.END, f"{rows} x {cols} matrix\n\n")
    # include ASCII representation
    for r in range(rows):
        text_widget.insert(tk.END, "  ".join(format_number(mat[r, c]).rjust(8) for c in range(cols)) + "\n")

def format_number(x):
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    s = f"{x:.6f}".rstrip('0').rstrip('.')
    return s

def do_binary_op(op):
    a_text = txtA.get("1.0", tk.END)
    b_text = txtB.get("1.0", tk.END)
    try:
        A = parse_matrix_from_text(a_text)
        B = parse_matrix_from_text(b_text)
    except Exception as e:
        messagebox.showerror("Input error", str(e))
        return
    try:
        if op == "add":
            if A.shape != B.shape:
                raise ValueError("Addition requires matrices of equal shape.")
            R = A + B
            display_result_matrix(R, tree_result, txt_result, lbl_det)
        elif op == "sub":
            if A.shape != B.shape:
                raise ValueError("Subtraction requires matrices of equal shape.")
            R = A - B
            display_result_matrix(R, tree_result, txt_result, lbl_det)
        elif op == "mul":
            if A.shape[1] != B.shape[0]:
                raise ValueError("Multiplication requires A.columns == B.rows.")
            R = A @ B
            display_result_matrix(R, tree_result, txt_result, lbl_det)
    except Exception as e:
        messagebox.showerror("Operation error", str(e))

def do_transpose(which):
    try:
        text = txtA.get("1.0", tk.END) if which == 'A' else txtB.get("1.0", tk.END)
        M = parse_matrix_from_text(text)
    except Exception as e:
        messagebox.showerror("Input error", str(e))
        return
    display_result_matrix(M.T, tree_result, txt_result, lbl_det)

def do_determinant(which):
    try:
        text = txtA.get("1.0", tk.END) if which == 'A' else txtB.get("1.0", tk.END)
        M = parse_matrix_from_text(text)
    except Exception as e:
        messagebox.showerror("Input error", str(e))
        return
    if M.shape[0] != M.shape[1]:
        messagebox.showerror("Input error", "Determinant is defined only for square matrices.")
        return
    det = np.linalg.det(M)
    lbl_det.config(text=f"det({which}) = {format_number(det)}")

# Build GUI
root = tk.Tk()
root.title("Matrix Operations Tool")

frm = ttk.Frame(root, padding=8)
frm.grid(row=0, column=0, sticky="nsew")

# Matrix inputs
lblA = ttk.Label(frm, text="Matrix A (rows as lines, cols separated by space/comma)")
lblA.grid(row=0, column=0, sticky="w")
txtA = tk.Text(frm, width=40, height=10)
txtA.grid(row=1, column=0, padx=4, pady=4)

lblB = ttk.Label(frm, text="Matrix B (rows as lines, cols separated by space/comma)")
lblB.grid(row=0, column=1, sticky="w")
txtB = tk.Text(frm, width=40, height=10)
txtB.grid(row=1, column=1, padx=4, pady=4)

# Buttons
btn_frame = ttk.Frame(frm)
btn_frame.grid(row=2, column=0, columnspan=2, pady=6)

ttk.Button(btn_frame, text="A + B", width=12, command=lambda: do_binary_op("add")).grid(row=0, column=0, padx=4, pady=2)
ttk.Button(btn_frame, text="A - B", width=12, command=lambda: do_binary_op("sub")).grid(row=0, column=1, padx=4, pady=2)
ttk.Button(btn_frame, text="A @ B", width=12, command=lambda: do_binary_op("mul")).grid(row=0, column=2, padx=4, pady=2)
ttk.Button(btn_frame, text="Aᵀ", width=12, command=lambda: do_transpose('A')).grid(row=0, column=3, padx=4, pady=2)
ttk.Button(btn_frame, text="Bᵀ", width=12, command=lambda: do_transpose('B')).grid(row=0, column=4, padx=4, pady=2)
ttk.Button(btn_frame, text="det(A)", width=12, command=lambda: do_determinant('A')).grid(row=1, column=0, padx=4, pady=2)
ttk.Button(btn_frame, text="det(B)", width=12, command=lambda: do_determinant('B')).grid(row=1, column=1, padx=4, pady=2)
ttk.Button(btn_frame, text="Clear Result", width=12, command=lambda: display_result_matrix(None, tree_result, txt_result, lbl_det)).grid(row=1, column=2, padx=4, pady=2)

# Result area
res_frame = ttk.LabelFrame(frm, text="Result")
res_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=8)

txt_result = tk.Text(res_frame, width=80, height=8)
txt_result.grid(row=0, column=0, padx=4, pady=4)

tree_result = ttk.Treeview(res_frame, show='headings')
tree_result.grid(row=1, column=0, padx=4, pady=4, sticky="nsew")

lbl_det = ttk.Label(res_frame, text="", font=("Segoe UI", 10, "bold"))
lbl_det.grid(row=2, column=0, sticky="w", padx=4, pady=4)

root.mainloop()
