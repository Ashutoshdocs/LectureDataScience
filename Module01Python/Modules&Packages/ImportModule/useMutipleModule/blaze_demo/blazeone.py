#!/usr/bin/env python3
"""
BlazeOne  -  Smart Calculator & Unit Converter
===============================================
A fully working, standalone, interactive terminal app.

Run it on its own:
    python blazeone.py

Or borrow its components from another file:
    from blazeone import banner, Calculator
"""

import ast
import math
import operator
import os

__all__ = ["banner", "gradient_text", "Calculator", "UnitConverter"]

os.system("")  # switches on ANSI colour support in Windows terminals

RESET, BOLD, DIM = "\033[0m", "\033[1m", "\033[2m"
FIRE = [196, 202, 208, 214, 220, 226]  # red -> orange -> yellow


def color(n):
    """Return the ANSI code for a 256-colour foreground."""
    return f"\033[38;5;{n}m"


def ask(prompt):
    """input() that treats Ctrl+C / Ctrl+D as 'go back'."""
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return "q"


# --------------------------------------------------------------------------
# COMPONENT 1: banner  (imported by BlazeFinal)
# --------------------------------------------------------------------------
def gradient_text(text, palette=FIRE):
    """Colour each character of `text` along a 256-colour palette."""
    if not text:
        return ""
    out = []
    for i, ch in enumerate(text):
        idx = round(i / max(len(text) - 1, 1) * (len(palette) - 1))
        out.append(color(palette[idx]) + ch)
    return "".join(out) + RESET


def banner(title, subtitle="", palette=FIRE, width=56):
    """Print a rounded box with a gradient title and a dim subtitle."""
    inner = width - 2
    edge = color(palette[0])
    spaced = " ".join(title.upper())
    rows = [(spaced, lambda t: BOLD + gradient_text(t, palette)),
            (subtitle, lambda t: DIM + t + RESET)]
    print()
    print(edge + "╭" + "─" * inner + "╮" + RESET)
    for text, style in rows:
        if not text:
            continue
        pad = inner - len(text)
        left = pad // 2
        print(edge + "│" + RESET + " " * left + style(text)
              + " " * (pad - left) + edge + "│" + RESET)
    print(edge + "╰" + "─" * inner + "╯" + RESET)


# --------------------------------------------------------------------------
# COMPONENT 2: Calculator  (imported by BlazeFinal)
# --------------------------------------------------------------------------
class Calculator:
    """Safe expression calculator with history and an `ans` variable.

    calc = Calculator()
    calc.evaluate("2 * (3 + 4)")   # -> 14
    calc.run()                     # interactive prompt
    """

    _OPS = {
        ast.Add: operator.add, ast.Sub: operator.sub,
        ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod,
        ast.Pow: operator.pow, ast.USub: operator.neg, ast.UAdd: operator.pos,
    }
    _FUNCS = {
        "sqrt": math.sqrt, "sin": lambda d: math.sin(math.radians(d)),
        "cos": lambda d: math.cos(math.radians(d)),
        "tan": lambda d: math.tan(math.radians(d)),
        "log": math.log10, "ln": math.log, "abs": abs, "round": round,
    }
    _CONSTS = {"pi": math.pi, "e": math.e}

    def __init__(self, accent=214):
        self.accent = accent
        self.history = []
        self.ans = 0

    # --- the engine (no eval(), parsed safely with ast) -------------------
    def evaluate(self, expression):
        tree = ast.parse(expression.replace("^", "**"), mode="eval")
        result = self._eval(tree.body)
        self.ans = result
        self.history.append((expression, result))
        return result

    def _eval(self, node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in self._OPS:
            left, right = self._eval(node.left), self._eval(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 1000:
                raise ValueError("exponent too large")
            return self._OPS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in self._OPS:
            return self._OPS[type(node.op)](self._eval(node.operand))
        if isinstance(node, ast.Name):
            if node.id == "ans":
                return self.ans
            if node.id in self._CONSTS:
                return self._CONSTS[node.id]
            raise ValueError(f"unknown name '{node.id}'")
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id in self._FUNCS and not node.keywords):
            return self._FUNCS[node.func.id](*[self._eval(a) for a in node.args])
        raise ValueError("unsupported expression")

    @staticmethod
    def fmt(n):
        if isinstance(n, float):
            if n.is_integer() and abs(n) < 1e15:
                return str(int(n))
            return f"{n:.10g}"
        return str(n)

    # --- the interactive screen -------------------------------------------
    def run(self):
        a = color(self.accent)
        print(f"\n  {a}{BOLD}▌ CALCULATOR{RESET}  {DIM}type 'help' for tips, 'back' to leave{RESET}\n")
        while True:
            expr = ask(f"  {a}calc ❯{RESET} ")
            low = expr.lower()
            if not expr:
                continue
            if low in ("back", "exit", "quit", "q"):
                break
            if low == "help":
                print(f"  {DIM}Operators : + - * / // % ** (or ^)\n"
                      f"  Functions : sqrt() sin() cos() tan() (degrees) log() ln() abs() round()\n"
                      f"  Extras    : pi, e, ans (last result), 'history', 'clear'{RESET}")
                continue
            if low == "history":
                if not self.history:
                    print(f"  {DIM}No calculations yet.{RESET}")
                for i, (e, r) in enumerate(self.history[-10:], 1):
                    print(f"  {DIM}{i:>2}.{RESET} {e} {DIM}={RESET} {a}{self.fmt(r)}{RESET}")
                continue
            if low == "clear":
                self.history.clear()
                print(f"  {DIM}History cleared.{RESET}")
                continue
            try:
                result = self.evaluate(expr)
                print(f"  {DIM}{expr} ={RESET} {BOLD}{color(46)}{self.fmt(result)}{RESET}")
            except ZeroDivisionError:
                print(f"  {color(196)}✖ Can't divide by zero{RESET}")
            except (ValueError, SyntaxError, TypeError, OverflowError) as exc:
                print(f"  {color(196)}✖ {exc or 'invalid input'}{RESET}")


# --------------------------------------------------------------------------
# BlazeOne-only feature: UnitConverter  (not used by BlazeFinal)
# --------------------------------------------------------------------------
class UnitConverter:
    UNITS = {
        "1": ("Kilometres → Miles", lambda v: v * 0.621371, "mi"),
        "2": ("Miles → Kilometres", lambda v: v / 0.621371, "km"),
        "3": ("Celsius → Fahrenheit", lambda v: v * 9 / 5 + 32, "°F"),
        "4": ("Fahrenheit → Celsius", lambda v: (v - 32) * 5 / 9, "°C"),
        "5": ("Kilograms → Pounds", lambda v: v * 2.20462, "lb"),
        "6": ("Pounds → Kilograms", lambda v: v / 2.20462, "kg"),
    }

    def run(self):
        while True:
            print(f"\n  {color(208)}{BOLD}▌ UNIT CONVERTER{RESET}")
            for key, (name, _, _) in self.UNITS.items():
                print(f"   {color(220)}{key}{RESET}  {name}")
            print(f"   {color(220)}0{RESET}  {DIM}Back{RESET}")
            choice = ask(f"  {color(208)}pick ❯{RESET} ")
            if choice in ("0", "q", "back"):
                break
            if choice not in self.UNITS:
                print(f"  {color(196)}✖ Choose 0-6{RESET}")
                continue
            name, fn, unit = self.UNITS[choice]
            raw = ask(f"  {DIM}{name.split(' → ')[0]}:{RESET} ")
            try:
                print(f"  {BOLD}{color(46)}= {fn(float(raw)):.2f} {unit}{RESET}")
            except ValueError:
                print(f"  {color(196)}✖ Please enter a number{RESET}")


# --------------------------------------------------------------------------
# The standalone app
# --------------------------------------------------------------------------
def main():
    calc = Calculator()
    banner("BlazeOne", "Smart Calculator & Unit Converter")
    while True:
        print(f"\n   {color(220)}1{RESET}  Calculator"
              f"\n   {color(220)}2{RESET}  Unit converter"
              f"\n   {color(220)}3{RESET}  About this module"
              f"\n   {color(220)}0{RESET}  {DIM}Exit{RESET}")
        choice = ask(f"\n  {color(202)}blazeone ❯{RESET} ")
        if choice == "1":
            calc.run()
        elif choice == "2":
            UnitConverter().run()
        elif choice == "3":
            print(f"\n  {DIM}Importable components:{RESET} {BOLD}{', '.join(__all__)}{RESET}"
                  f"\n  {DIM}Try:{RESET} from blazeone import banner, Calculator")
        elif choice in ("0", "q", "exit"):
            print("\n  " + gradient_text("Thanks for using BlazeOne. Stay blazing!") + "\n")
            break
        else:
            print(f"  {color(196)}✖ Choose 0-3{RESET}")


# Runs ONLY when started directly (python blazeone.py),
# NOT when another file does `from blazeone import ...`
if __name__ == "__main__":
    main()
