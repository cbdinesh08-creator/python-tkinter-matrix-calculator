import tkinter as tk
from tkinter import ttk, messagebox


# ---------- MATRIX CALCULATION FUNCTIONS ----------

def multiply(A, B):
    if len(A[0]) != len(B):
        raise ValueError(
            "Multiplication is not possible.\n"
            "Columns of Matrix A must equal rows of Matrix B."
        )

    result = []

    for i in range(len(A)):
        row = []

        for j in range(len(B[0])):
            total = 0

            for k in range(len(B)):
                total += A[i][k] * B[k][j]

            row.append(total)

        result.append(row)

    return result


def square(A):
    if len(A) != len(A[0]):
        raise ValueError(
            "Squaring is possible only for a square matrix."
        )

    return multiply(A, A)


def determinant(A):
    n = len(A)

    if n == 1:
        return A[0][0]

    if n == 2:
        return (
            A[0][0] * A[1][1]
            - A[0][1] * A[1][0]
        )

    det = 0

    for j in range(n):
        minor = [
            row[:j] + row[j + 1:]
            for row in A[1:]
        ]

        det += (
            (-1) ** j
            * A[0][j]
            * determinant(minor)
        )

    return det


def adjoint(A):
    n = len(A)

    if n == 1:
        return [[1]]

    cofactors = []

    for i in range(n):
        row = []

        for j in range(n):
            minor = [
                r[:j] + r[j + 1:]
                for k, r in enumerate(A)
                if k != i
            ]

            cofactor = (
                (-1) ** (i + j)
                * determinant(minor)
            )

            row.append(cofactor)

        cofactors.append(row)

    return [list(row) for row in zip(*cofactors)]


def inverse(A):
    det = determinant(A)

    if det == 0:
        raise ValueError(
            "Inverse does not exist because "
            "the determinant is zero."
        )

    adj = adjoint(A)

    return [
        [adj[i][j] / det for j in range(len(A))]
        for i in range(len(A))
    ]


# ---------- MAIN WINDOW ----------

root = tk.Tk()
root.title("Matrix Calculator")
root.geometry("950x720")
root.minsize(800, 620)

style = ttk.Style()
style.configure(
    "Title.TLabel",
    font=("Arial", 20, "bold")
)
style.configure(
    "TButton",
    font=("Arial", 10),
    padding=6
)

ttk.Label(
    root,
    text="MATRIX CALCULATOR",
    style="Title.TLabel"
).pack(pady=12)

ttk.Label(
    root,
    text="Square | Multiplication | Determinant | Inverse | Adjoint"
).pack(pady=3)


# ---------- MATRIX INPUT INTERFACE ----------

matrix_data = {}

matrix_frame = ttk.Frame(root, padding=10)
matrix_frame.pack(fill="x")


def create_matrix_panel(name, column):
    panel = ttk.LabelFrame(
        matrix_frame,
        text="Matrix " + name,
        padding=10
    )
    panel.grid(
        row=0,
        column=column,
        padx=10,
        sticky="nsew"
    )

    rows_var = tk.StringVar(value="2")
    cols_var = tk.StringVar(value="2")

    ttk.Label(panel, text="Rows").grid(
        row=0, column=0, padx=4
    )

    ttk.Spinbox(
        panel,
        from_=1,
        to=8,
        width=5,
        textvariable=rows_var
    ).grid(row=0, column=1, padx=4)

    ttk.Label(panel, text="Columns").grid(
        row=0, column=2, padx=4
    )

    ttk.Spinbox(
        panel,
        from_=1,
        to=8,
        width=5,
        textvariable=cols_var
    ).grid(row=0, column=3, padx=4)

    input_frame = ttk.Frame(panel)
    input_frame.grid(
        row=2,
        column=0,
        columnspan=4,
        pady=8
    )

    matrix_data[name] = {
        "rows": rows_var,
        "cols": cols_var,
        "frame": input_frame,
        "entries": []
    }

    def generate():
        try:
            rows = int(rows_var.get())
            cols = int(cols_var.get())

            if not (
                1 <= rows <= 8
                and 1 <= cols <= 8
            ):
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Dimensions",
                "Enter rows and columns between 1 and 8."
            )
            return

        for widget in input_frame.winfo_children():
            widget.destroy()

        entries = []

        for i in range(rows):
            entry_row = []

            for j in range(cols):
                entry = ttk.Entry(
                    input_frame,
                    width=7,
                    justify="center"
                )
                entry.grid(
                    row=i,
                    column=j,
                    padx=3,
                    pady=3
                )
                entry.insert(0, "0")
                entry_row.append(entry)

            entries.append(entry_row)

        matrix_data[name]["entries"] = entries

    ttk.Button(
        panel,
        text="Generate Matrix",
        command=generate
    ).grid(
        row=1,
        column=0,
        columnspan=4,
        pady=5
    )

    generate()


matrix_frame.columnconfigure(0, weight=1)
matrix_frame.columnconfigure(1, weight=1)

create_matrix_panel("A", 0)
create_matrix_panel("B", 1)


# ---------- READ MATRIX VALUES ----------

def get_matrix(name):
    entries = matrix_data[name]["entries"]

    if not entries:
        raise ValueError(
            "Generate Matrix " + name + " first."
        )

    matrix = []

    for i, row in enumerate(entries):
        values = []

        for j, entry in enumerate(row):
            try:
                value = int(entry.get().strip())

            except ValueError:
                raise ValueError(
                    f"Matrix {name}: enter an integer "
                    f"at row {i + 1}, column {j + 1}."
                )

            values.append(value)

        matrix.append(values)

    return matrix


# ---------- DISPLAY RESULT ----------

result_frame = ttk.LabelFrame(
    root,
    text="Result / Output",
    padding=10
)
result_frame.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)

result_box = tk.Text(
    result_frame,
    height=6,
    font=("Consolas", 12),
    wrap="none"
)
result_box.pack(fill="both", expand=True)


def show_result(title, result):
    result_box.delete("1.0", tk.END)

    result_box.insert(tk.END, title + "\n")
    result_box.insert(tk.END, "-" * 40 + "\n")

    if isinstance(result, list):
        for row in result:
            formatted = []

            for value in row:
                if isinstance(value, float):
                    if abs(value) < 1e-10:
                        value = 0.0

                    formatted.append(f"{value:.4f}")

                else:
                    formatted.append(str(value))

            result_box.insert(
                tk.END,
                "   ".join(formatted) + "\n"
            )

    else:
        result_box.insert(
            tk.END,
            str(result) + "\n"
        )


# ---------- OPERATION BUTTONS ----------

def run_operation(operation, name=None):
    try:
        if operation == "multiply":
            A = get_matrix("A")
            B = get_matrix("B")

            result = multiply(A, B)
            title = "Matrix A x Matrix B"

        else:
            A = get_matrix(name)

            if (
                len(A) != len(A[0])
                and operation != "square"
            ):
                raise ValueError(
                    "This operation requires a square matrix."
                )

            if operation == "square":
                result = square(A)
                title = "Square of Matrix " + name

            elif operation == "determinant":
                result = determinant(A)
                title = "Determinant of Matrix " + name

            elif operation == "inverse":
                result = inverse(A)
                title = "Inverse of Matrix " + name

            elif operation == "adjoint":
                result = adjoint(A)
                title = "Adjoint of Matrix " + name

            else:
                return

        show_result(title, result)

    except ValueError as error:
        messagebox.showwarning(
            "Operation Error",
            str(error)
        )


# ---------- BUTTON LAYOUT ----------

button_frame = ttk.LabelFrame(
    root,
    text="Select Operation",
    padding=10
)
button_frame.pack(
    fill="x",
    padx=15,
    pady=5
)

buttons = [
    ("Square A", lambda: run_operation("square", "A")),
    ("Square B", lambda: run_operation("square", "B")),
    ("Multiply A x B", lambda: run_operation("multiply")),
    ("Determinant A", lambda: run_operation("determinant", "A")),
    ("Determinant B", lambda: run_operation("determinant", "B")),
    ("Inverse A", lambda: run_operation("inverse", "A")),
    ("Inverse B", lambda: run_operation("inverse", "B")),
    ("Adjoint A", lambda: run_operation("adjoint", "A")),
    ("Adjoint B", lambda: run_operation("adjoint", "B"))
]

for i, (label, command) in enumerate(buttons):
    ttk.Button(
        button_frame,
        text=label,
        command=command
    ).grid(
        row=i // 3,
        column=i % 3,
        padx=5,
        pady=5,
        sticky="ew"
    )

for column in range(3):
    button_frame.columnconfigure(
        column,
        weight=1
    )


# ---------- CLEAR AND EXIT BUTTONS ----------

bottom_frame = ttk.Frame(root, padding=10)
bottom_frame.pack(fill="x")


ttk.Button(
    bottom_frame,
    text="Clear Result",
    command=lambda: result_box.delete("1.0", tk.END)
).pack(side="left", padx=5)

ttk.Button(
    bottom_frame,
    text="Exit",
    command=root.destroy
).pack(side="right", padx=5)


root.mainloop()
