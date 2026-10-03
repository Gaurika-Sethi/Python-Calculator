import tkinter as tk
import math

class GateCalculator:
    def __init__(self, root):
        self.root = root
        root.title("GATE Scientific Calculator")
        root.geometry("360x520")
        root.resizable(False, False)
        root.attributes("-topmost", True)

        self.expr = tk.StringVar()
        self.mode = tk.StringVar(value="DEG")

        display = tk.Entry(
            root, textvariable=self.expr, font=("Segoe UI", 18),
            justify="right", bd=2, relief="sunken"
        )
        display.pack(fill="x", padx=10, pady=(10, 5), ipady=8)
        display.focus_set()

        top = tk.Frame(root)
        top.pack(fill="x", padx=10, pady=3)

        tk.Button(top, text="Always on top: ON", command=self.toggle_top,
                  font=("Segoe UI", 9)).pack(side="left", padx=(0, 5))
        tk.Button(top, textvariable=self.mode, command=self.toggle_mode,
                  width=6).pack(side="right")

        keys = [
            ["sin", "cos", "tan", "log", "ln"],
            ["asin", "acos", "atan", "sqrt", "x²"],
            ["7", "8", "9", "(", ")"],
            ["4", "5", "6", "^", "÷"],
            ["1", "2", "3", "+", "-"],
            ["0", ".", "π", "e", "="],
            ["C", "⌫", "1/x", "x!", "%"],
        ]

        frame = tk.Frame(root)
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        for r, row in enumerate(keys):
            for c, key in enumerate(row):
                b = tk.Button(
                    frame, text=key, font=("Segoe UI", 11),
                    command=lambda k=key: self.press(k)
                )
                b.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)

        for i in range(7):
            frame.rowconfigure(i, weight=1)
        for i in range(5):
            frame.columnconfigure(i, weight=1)

        root.bind("<Return>", lambda e: self.press("="))
        root.bind("<Escape>", lambda e: self.press("C"))
        root.bind("<BackSpace>", lambda e: self.press("⌫"))

    def toggle_top(self):
        current = self.root.attributes("-topmost")
        self.root.attributes("-topmost", not current)

    def toggle_mode(self):
        self.mode.set("RAD" if self.mode.get() == "DEG" else "DEG")

    def press(self, key):
        s = self.expr.get()

        if key == "^":
            key = "**"

        if key == "C":
            self.expr.set("")
            return
        if key == "⌫":
            self.expr.set(s[:-1])
            return
        if key == "=":
            self.calculate()
            return

        if key == "×":
            key = "*"
        elif key == "÷":
            key = "/"
        elif key == "π":
            key = "pi"
        elif key == "x²":
            key = "**2"
        elif key == "sqrt":
            key = "sqrt("
        elif key in ("sin", "cos", "tan", "asin", "acos", "atan", "log", "ln"):
            key += "("
        elif key == "1/x":
            if s:
                self.expr.set(f"1/({s})")
            return
        elif key == "x!":
            if s:
                self.expr.set(f"factorial({s})")
            return
        elif key == "%":
            key = "/100"
        elif key == "e":
            key = "e"

        self.expr.set(s + key)

    def calculate(self):
        try:
            expression = self.expr.get()

            angle_mode = self.mode.get()

            def sin(x):
                return math.sin(math.radians(x)) if angle_mode == "DEG" else math.sin(x)
            def cos(x):
                return math.cos(math.radians(x)) if angle_mode == "DEG" else math.cos(x)
            def tan(x):
                return math.tan(math.radians(x)) if angle_mode == "DEG" else math.tan(x)
            def asin(x):
                v = math.asin(x)
                return math.degrees(v) if angle_mode == "DEG" else v
            def acos(x):
                v = math.acos(x)
                return math.degrees(v) if angle_mode == "DEG" else v
            def atan(x):
                v = math.atan(x)
                return math.degrees(v) if angle_mode == "DEG" else v

            env = {
                "__builtins__": {},
                "sin": sin, "cos": cos, "tan": tan,
                "asin": asin, "acos": acos, "atan": atan,
                "log": math.log10, "ln": math.log,
                "sqrt": math.sqrt, "factorial": math.factorial,
                "pi": math.pi, "e": math.e
            }

            result = eval(expression, env, {})
            if isinstance(result, float):
                if abs(result) < 1e-12:
                    result = 0
                result = round(result, 12)

            self.expr.set(str(result))

        except Exception:
            self.expr.set("Error")

if __name__ == "__main__":
    root = tk.Tk()
    GateCalculator(root)
    root.mainloop()
