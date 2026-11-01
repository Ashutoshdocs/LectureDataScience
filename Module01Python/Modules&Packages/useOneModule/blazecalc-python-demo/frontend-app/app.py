"""Interactive BlazeCalc desktop app (Tkinter).

The UI lives here in frontend-app/. ALL the math comes from the BlazeCalc
module in the other folder, installed with:  pip install -e ../BlazeCalc
"""

import tkinter as tk

# ⭐ The important line: importing the module from the other folder.
import BlazeCalc
# You can also pick individual pieces:
# from BlazeCalc import evaluate, sqrt, Calculator

# ---- Theme ------------------------------------------------------------------
BG = "#0f1115"
PANEL = "#1a1d24"
KEY = "#262a33"
KEY_HOVER = "#343945"
ACCENT = "#ff6b2c"
TEXT = "#f2f2f2"
MUTED = "#9aa0aa"
ERROR = "#ff5c5c"

# Button layout: (label, kind). The "=" row spans the full width.
BUTTONS = [
    [("C", "fn"), ("DEL", "fn"), ("%", "fn"), ("÷", "op")],
    [("7", "num"), ("8", "num"), ("9", "num"), ("×", "op")],
    [("4", "num"), ("5", "num"), ("6", "num"), ("-", "op")],
    [("1", "num"), ("2", "num"), ("3", "num"), ("+", "op")],
    [("0", "num"), (".", "num"), ("(", "fn"), (")", "fn")],
    [("√", "fn"), ("x²", "fn"), ("±", "fn"), ("=", "eq")],
]


class BlazeCalcApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"🔥 BlazeCalc v{BlazeCalc.__version__}")
        self.configure(bg=BG, padx=16, pady=16)
        self.minsize(560, 460)

        # A BlazeCalc Calculator object keeps our history for us
        self.calc = BlazeCalc.Calculator()
        self.just_evaluated = False

        self.expression = tk.StringVar()
        self.preview = tk.StringVar()
        self.status = tk.StringVar()

        self._build_ui()
        self._bind_keys()
        self.expression.trace_add("write", lambda *_: self._live_preview())

    # ---- UI -----------------------------------------------------------------
    def _build_ui(self):
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)

        # Left: the calculator
        left = tk.Frame(self, bg=PANEL, padx=14, pady=14)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        entry = tk.Entry(
            left, textvariable=self.expression, font=("Helvetica", 24),
            bg="#0b0d10", fg=TEXT, insertbackground=ACCENT, relief="flat",
            justify="right",
        )
        entry.pack(fill="x", ipady=10)
        entry.focus_set()
        self.entry = entry

        tk.Label(left, textvariable=self.preview, font=("Helvetica", 13),
                 bg=PANEL, fg=MUTED, anchor="e").pack(fill="x", pady=(4, 0))
        tk.Label(left, textvariable=self.status, font=("Helvetica", 11),
                 bg=PANEL, fg=ERROR, anchor="e").pack(fill="x")

        keys = tk.Frame(left, bg=PANEL)
        keys.pack(fill="both", expand=True, pady=(8, 0))
        for r, row in enumerate(BUTTONS):
            keys.rowconfigure(r, weight=1, uniform="row")
            for c, (label, kind) in enumerate(row):
                keys.columnconfigure(c, weight=1, uniform="col")
                self._make_button(keys, label, kind).grid(
                    row=r, column=c, sticky="nsew", padx=3, pady=3)

        # Right: history
        right = tk.Frame(self, bg=PANEL, padx=14, pady=14)
        right.grid(row=0, column=1, sticky="nsew")

        tk.Label(right, text="History", font=("Helvetica", 15, "bold"),
                 bg=PANEL, fg=TEXT, anchor="w").pack(fill="x")
        tk.Label(right, text="Click an item to reuse its result",
                 font=("Helvetica", 10), bg=PANEL, fg=MUTED, anchor="w",
                 justify="left", wraplength=160).pack(fill="x")

        self.history_box = tk.Listbox(
            right, bg="#0b0d10", fg=TEXT, font=("Courier", 12), relief="flat",
            selectbackground=ACCENT, highlightthickness=0, activestyle="none",
        )
        self.history_box.pack(fill="both", expand=True, pady=8)
        self.history_box.bind("<<ListboxSelect>>", self._reuse_history)

        tk.Button(right, text="Clear history", command=self._clear_history,
                  bg=KEY, fg=MUTED, relief="flat", activebackground=KEY_HOVER,
                  activeforeground=TEXT, cursor="hand2").pack(fill="x")

    def _make_button(self, parent, label, kind):
        colors = {
            "num": (KEY, TEXT),
            "op": (KEY, ACCENT),
            "fn": (KEY, MUTED),
            "eq": (ACCENT, "#ffffff"),
        }
        bg, fg = colors[kind]
        btn = tk.Button(
            parent, text=label, font=("Helvetica", 18), bg=bg, fg=fg,
            activebackground=KEY_HOVER if kind != "eq" else "#ff8a55",
            activeforeground=fg, relief="flat", bd=0, cursor="hand2",
            highlightthickness=0,
            command=lambda: self.press(label),
        )
        # Simple hover effect
        hover = KEY_HOVER if kind != "eq" else "#ff8a55"
        btn.bind("<Enter>", lambda e: btn.configure(bg=hover))
        btn.bind("<Leave>", lambda e: btn.configure(bg=bg))
        return btn

    def _bind_keys(self):
        self.bind("<Return>", lambda e: self.press("="))
        self.bind("<KP_Enter>", lambda e: self.press("="))
        self.bind("<Escape>", lambda e: self.press("C"))
        self.bind("<Delete>", lambda e: self.press("C"))

    # ---- Behaviour (every calculation goes through BlazeCalc) ---------------
    def press(self, key):
        self.status.set("")
        text = self.expression.get()

        if key == "C":
            self.expression.set("")
        elif key == "DEL":
            self.expression.set(text[:-1])
        elif key == "=":
            self.calculate()
            return
        elif key in ("√", "x²", "%", "±"):
            self._apply_function(key, text)
            return
        else:
            # Start fresh if the user types a digit right after a result
            if self.just_evaluated and key not in ("+", "-", "×", "÷"):
                text = ""
            self.expression.set(text + key)

        self.just_evaluated = False
        self.entry.icursor("end")

    def _apply_function(self, key, text):
        """Functions that act on the current value."""
        try:
            value = BlazeCalc.evaluate(text) if text else 0
            # Wrap in brackets only if needed: "9" stays "9", "2+3" becomes "(2+3)"
            simple = text.startswith("(") and text.endswith(")") or \
                text.replace(".", "").isdigit()
            shown = (text or "0") if simple else f"({text})"
            if key == "√":
                result, label = BlazeCalc.sqrt(value), f"√{shown}"
            elif key == "x²":
                result, label = BlazeCalc.power(value, 2), f"{shown}²"
            elif key == "%":
                result, label = BlazeCalc.percent(value, 1), f"{shown}%"
            else:  # ±
                result, label = BlazeCalc.multiply(value, -1), f"-{shown}"
            result = BlazeCalc.evaluate(str(result))  # tidy formatting
            self._show_result(label, result)
        except (ValueError, TypeError, ZeroDivisionError) as err:
            self.status.set(str(err))

    def calculate(self):
        text = self.expression.get().strip()
        if not text:
            return
        try:
            result = BlazeCalc.evaluate(text)  # 👈 BlazeCalc does the work
            self._show_result(text, result)
        except (ValueError, TypeError, ZeroDivisionError, OverflowError) as err:
            self.status.set(str(err))

    def _show_result(self, label, result):
        self.calc.record(label, result)
        self.history_box.insert(0, f"{label} = {result}")
        self.expression.set(str(result))
        self.preview.set("")
        self.just_evaluated = True
        self.entry.icursor("end")

    def _live_preview(self):
        """Show the answer as you type (silently ignore half-typed input)."""
        text = self.expression.get().strip()
        try:
            result = BlazeCalc.evaluate(text)
            self.preview.set("" if str(result) == text else f"= {result}")
        except Exception:
            self.preview.set("")

    def _reuse_history(self, _event):
        sel = self.history_box.curselection()
        if sel:
            line = self.history_box.get(sel[0])
            self.expression.set(line.rsplit("= ", 1)[-1])
            self.just_evaluated = True
            self.entry.focus_set()
            self.entry.icursor("end")

    def _clear_history(self):
        self.calc.clear()
        self.history_box.delete(0, "end")


if __name__ == "__main__":
    BlazeCalcApp().mainloop()
