#!/usr/bin/env python3
"""
Matrix Operations Tool (CLI)
Supports: addition, subtraction, multiplication, transpose, determinant
Input format: provide number of rows/cols and then rows with space/comma-separated numbers
"""
import numpy as np
import sys

def read_matrix(name="Matrix"):
    try:
        rows = int(input(f"Enter number of rows for {name}: ").strip())
        cols = int(input(f"Enter number of columns for {name}: ").strip())
    except ValueError:
        print("Invalid integer for rows/columns. Try again.")
        return read_matrix(name)

    print(f"Enter {rows} rows. Separate values by space or comma.")
    data = []
    for r in range(rows):
        while True:
            line = input(f"Row {r+1}: ").strip()
            if not line:
                print("Empty row — please enter the numbers.")
                continue
            # split on spaces or commas
            parts = [p for p in line.replace(',', ' ').split() if p]
            if len(parts) != cols:
                print(f"Expected {cols} values but got {len(parts)}. Try again.")
                continue
            try:
                row = [float(x) for x in parts]
            except ValueError:
                print("Non-numeric value found. Try again.")
                continue
            data.append(row)
            break
    return np.array(data, dtype=float)

def pretty_print(mat, name="Result"):
    if mat.ndim == 0:
        print(f"{name}: {mat}")
        return
    # Determine column widths
    rows, cols = mat.shape
    str_mat = [[format_number(mat[r,c]) for c in range(cols)] for r in range(rows)]
    col_widths = [max(len(str_mat[r][c]) for r in range(rows)) for c in range(cols)]
    print(f"\n{name} ({rows} x {cols}):")
    for r in range(rows):
        row_str = "  ".join(str_mat[r][c].rjust(col_widths[c]) for c in range(cols))
        print(row_str)
    print("")

def format_number(x):
    # If it's effectively integer, show as int
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    # else show up to 6 significant digits but remove trailing zeros
    s = f"{x:.6f}".rstrip('0').rstrip('.')
    return s

def main_menu():
    print("Matrix Operations Tool (CLI)")
    print("----------------------------")
    print("You will be asked to input matrices when needed.")
    while True:
        print("\nAvailable operations:")
        print("1) Addition (A + B)")
        print("2) Subtraction (A - B)")
        print("3) Multiplication (A @ B)")
        print("4) Transpose (A^T or B^T)")
        print("5) Determinant (det(A) or det(B))")
        print("6) Exit")
        choice = input("Choose operation (1-6): ").strip()
        if choice == '6':
            print("Goodbye!")
            sys.exit(0)

        if choice in {'1','2','3'}:
            A = read_matrix("Matrix A")
            B = read_matrix("Matrix B")
            try:
                if choice == '1': # add
                    if A.shape != B.shape:
                        print("Addition requires matrices of same shape.")
                        continue
                    C = A + B
                    pretty_print(C, "A + B")
                elif choice == '2': # subtract
                    if A.shape != B.shape:
                        print("Subtraction requires matrices of same shape.")
                        continue
                    C = A - B
                    pretty_print(C, "A - B")
                else: # multiply
                    if A.shape[1] != B.shape[0]:
                        print("Multiplication requires A.columns == B.rows.")
                        continue
                    C = A @ B
                    pretty_print(C, "A @ B")
            except Exception as e:
                print("Error during operation:", e)

        elif choice == '4':  # transpose
            which = input("Transpose which matrix? (A/B): ").strip().upper()
            if which not in {'A','B'}:
                print("Choose A or B.")
                continue
            M = read_matrix(f"Matrix {which}")
            pretty_print(M.T, f"{which}^T")

        elif choice == '5':  # determinant
            which = input("Determinant of which matrix? (A/B): ").strip().upper()
            if which not in {'A','B'}:
                print("Choose A or B.")
                continue
            M = read_matrix(f"Matrix {which}")
            if M.shape[0] != M.shape[1]:
                print("Determinant defined only for square matrices.")
                continue
            det = np.linalg.det(M)
            print(f"det({which}) = {format_number(det)}")

        else:
            print("Invalid choice. Enter a number 1-6.")

if __name__ == "__main__":
    main_menu()
