
#!/usr/bin/env python3
# Shebang: tells Unix/Linux systems to execute this file using Python 3.

"""
BlazeOne - Smart Calculator & Unit Converter

A standalone interactive terminal application.

Run directly:
    python blazeone.py

Import components into another Python file:
    from blazeone import banner, Calculator
"""

import ast                  # Parses mathematical expressions into an Abstract Syntax Tree.
import math                 # Provides mathematical functions such as sqrt, sin, cos and pi.
import operator             # Provides operator functions such as add, sub, mul and div.
import os                   # Provides operating-system-related functionality.

# Defines the public names available through: from blazeone import *
__all__ = ["banner", "gradient_text", "Calculator", "UnitConverter"]

os.system("")               # Enables ANSI colour support in some Windows terminals.

# ANSI escape codes used for terminal text formatting.
RESET, BOLD, DIM = "\033[0m", "\033[1m", "\033[2m"

# Defines a 256-colour palette representing red, orange and yellow.
FIRE = [196, 202, 208, 214, 220, 226]


def color(n):
    """Return the ANSI escape code for a 256-colour foreground."""
    return f"\033[38;5;{n}m"  # Generates the terminal colour code.


def ask(prompt):
    """Read user input and treat Ctrl+C or Ctrl+D as a request to go back."""
    try:
        return input(prompt).strip()  # Reads input and removes surrounding whitespace.
    except (EOFError, KeyboardInterrupt):  # Handles Ctrl+D and Ctrl+C.
        print()                           # Moves to the next terminal line.
        return "q"                        # Returns q to trigger the exit/back logic.


# --------------------------------------------------------------------------
# COMPONENT 1: BANNER
# Reusable functions that can be imported into another Python file.
# --------------------------------------------------------------------------

def gradient_text(text, palette=FIRE):
    """Colour each character of text using a gradient palette."""

    if not text:                 # Checks whether the supplied text is empty.
        return ""                # Returns an empty string if there is no text.

    out = []                     # Creates a list to store coloured characters.

    for i, ch in enumerate(text):  # Loops through each character with its index.

        # Calculates which palette colour should be used for this character.
        idx = round(i / max(len(text) - 1, 1) * (len(palette) - 1))

        # Adds the colour code and character to the output list.
        out.append(color(palette[idx]) + ch)

    return "".join(out) + RESET  # Combines characters and resets terminal colour.


def banner(title, subtitle="", palette=FIRE, width=56):
    """Print a rounded terminal box with a gradient title."""

    inner = width - 2            # Calculates the inner width of the box.
    edge = color(palette[0])     # Selects the first palette colour for borders.

    spaced = " ".join(title.upper())  # Converts title to uppercase with spaces.

    # Stores title and subtitle along with their respective formatting functions.
    rows = [
        (spaced, lambda t: BOLD + gradient_text(t, palette)),
        (subtitle, lambda t: DIM + t + RESET)
    ]

    print()  # Adds an empty line before the banner.

    # Prints the top border of the box.
    print(edge + "╭" + "─" * inner + "╮" + RESET)

    # Processes the title and subtitle one row at a time.
    for text, style in rows:

        if not text:             # Checks whether the current row is empty.
            continue             # Skips empty rows.

        pad = inner - len(text)  # Calculates available padding space.
        left = pad // 2          # Calculates left-side padding for centering.

        # Prints the left border, centered content, right padding and right border.
        print(
            edge + "│" + RESET
            + " " * left
            + style(text)
            + " " * (pad - left)
            + edge + "│" + RESET
        )

    # Prints the bottom border of the box.
    print(edge + "╰" + "─" * inner + "╯" + RESET)


# --------------------------------------------------------------------------
# COMPONENT 2: CALCULATOR
# A reusable class that can be imported into another Python application.
# --------------------------------------------------------------------------

class Calculator:
    """Safe expression calculator with history and an ans variable."""

    # Maps Python AST mathematical operators to actual operator functions.
    _OPS = {
        ast.Add: operator.add,          # Handles addition (+).
        ast.Sub: operator.sub,          # Handles subtraction (-).
        ast.Mult: operator.mul,         # Handles multiplication (*).
        ast.Div: operator.truediv,     # Handles division (/).
        ast.FloorDiv: operator.floordiv,  # Handles floor division (//).
        ast.Mod: operator.mod,          # Handles modulus (%).
        ast.Pow: operator.pow,          # Handles exponentiation (**).
        ast.USub: operator.neg,         # Handles unary negative (-5).
        ast.UAdd: operator.pos          # Handles unary positive (+5).
    }

    # Defines mathematical functions that users are allowed to execute.
    _FUNCS = {
        "sqrt": math.sqrt,                           # Square root.
        "sin": lambda d: math.sin(math.radians(d)), # Sine in degrees.
        "cos": lambda d: math.cos(math.radians(d)), # Cosine in degrees.
        "tan": lambda d: math.tan(math.radians(d)), # Tangent in degrees.
        "log": math.log10,                           # Base-10 logarithm.
        "ln": math.log,                              # Natural logarithm.
        "abs": abs,                                  # Absolute value.
        "round": round                              # Rounds a number.
    }

    # Defines mathematical constants available to users.
    _CONSTS = {
        "pi": math.pi,  # Value of pi.
        "e": math.e     # Euler's number.
    }

    def __init__(self, accent=214):
        # Constructor: executes automatically when Calculator() is created.
        self.accent = accent   # Stores the terminal colour preference.
        self.history = []      # Creates an empty calculation history.
        self.ans = 0           # Stores the last calculated answer.

    # ---------------- CALCULATION ENGINE ----------------

    def evaluate(self, expression):
        # Replaces ^ with ** so users can write either exponent notation.
        tree = ast.parse(expression.replace("^", "**"), mode="eval")

        # Evaluates the parsed expression using our restricted AST evaluator.
        result = self._eval(tree.body)

        self.ans = result                 # Saves the result for future ans usage.
        self.history.append((expression, result))  # Adds expression and result to history.

        return result                     # Returns the calculated answer.

    def _eval(self, node):
        # Allows numeric constants such as 10, 20.5 and 100.
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value

        # Handles binary operations such as 10 + 20 or 5 * 4.
        if isinstance(node, ast.BinOp) and type(node.op) in self._OPS:

            left = self._eval(node.left)    # Evaluates the left operand.
            right = self._eval(node.right)  # Evaluates the right operand.

            # Prevents excessively large positive or negative exponents.
            if isinstance(node.op, ast.Pow) and abs(right) > 1000:
                raise ValueError("exponent too large")

            # Executes the corresponding mathematical operation.
            return self._OPS[type(node.op)](left, right)

        # Handles unary operations such as -5 and +10.
        if isinstance(node, ast.UnaryOp) and type(node.op) in self._OPS:
            return self._OPS[type(node.op)](self._eval(node.operand))

        # Handles variable names such as ans, pi and e.
        if isinstance(node, ast.Name):

            if node.id == "ans":        # Checks whether the user entered ans.
                return self.ans         # Returns the previous calculation result.

            if node.id in self._CONSTS: # Checks whether the name is a constant.
                return self._CONSTS[node.id]  # Returns its mathematical value.

            raise ValueError(f"unknown name '{node.id}'")  # Rejects unknown names.

        # Handles allowed function calls such as sqrt(25) and sin(30).
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in self._FUNCS
            and not node.keywords
        ):
            # Executes the permitted function with evaluated arguments.
            return self._FUNCS[node.func.id](
                *[self._eval(a) for a in node.args]
            )

        # Rejects expressions containing unsupported Python syntax.
        raise ValueError("unsupported expression")

    @staticmethod
    def fmt(n):
        # Static method: does not require access to self or an object instance.

        if isinstance(n, float):  # Checks whether the result is a float.

            if n.is_integer() and abs(n) < 1e15:
                return str(int(n))  # Displays whole-number floats as integers.

            return f"{n:.10g}"       # Formats decimal values neatly.

        return str(n)                # Converts other numeric results into strings.

    # ---------------- INTERACTIVE CALCULATOR SCREEN ----------------

    def run(self):
        # Retrieves the configured terminal colour for this calculator.
        a = color(self.accent)

        # Prints the calculator heading and instructions.
        print(
            f"\n  {a}{BOLD}▌ CALCULATOR{RESET}  "
            f"{DIM}type 'help' for tips, 'back' to leave{RESET}\n"
        )

        # Keeps accepting calculations until the user chooses to exit.
        while True:

            # Displays the calculator prompt and reads user input.
            expr = ask(f"  {a}calc ❯{RESET} ")

            low = expr.lower()  # Converts input to lowercase for comparison.

            if not expr:        # Checks whether the user entered nothing.
                continue        # Restarts the loop.

            # Checks whether the user wants to leave the calculator.
            if low in ("back", "exit", "quit", "q"):
                break

            # Displays help information when the user enters help.
            if low == "help":
                print(
                    f"  {DIM}Operators : + - * / // % ** (or ^)\n"
                    f"  Functions : sqrt() sin() cos() tan() (degrees) log() ln() abs() round()\n"
                    f"  Extras    : pi, e, ans (last result), 'history', 'clear'{RESET}"
                )
                continue

            # Displays the last 10 calculations when history is entered.
            if low == "history":

                if not self.history:
                    print(f"  {DIM}No calculations yet.{RESET}")

                for i, (e, r) in enumerate(self.history[-10:], 1):
                    print(
                        f"  {DIM}{i:>2}.{RESET} {e} "
                        f"{DIM}={RESET} {a}{self.fmt(r)}{RESET}"
                    )

                continue

            # Clears the calculation history when clear is entered.
            if low == "clear":
                self.history.clear()
                print(f"  {DIM}History cleared.{RESET}")
                continue

            # Attempts to calculate the supplied expression.
            try:
                result = self.evaluate(expr)

                # Displays the expression and its calculated result.
                print(
                    f"  {DIM}{expr} ={RESET} "
                    f"{BOLD}{color(46)}{self.fmt(result)}{RESET}"
                )

            # Handles division by zero separately.
            except ZeroDivisionError:
                print(f"  {color(196)}✖ Can't divide by zero{RESET}")

            # Handles invalid expressions and other calculation errors.
            except (ValueError, SyntaxError, TypeError, OverflowError) as exc:
                print(f"  {color(196)}✖ {exc or 'invalid input'}{RESET}")


# --------------------------------------------------------------------------
# COMPONENT 3: UNIT CONVERTER
# Converts distance, temperature and weight.
# --------------------------------------------------------------------------

class UnitConverter:

    # Stores conversion options using a dictionary.
    # Each key contains a description, conversion function and output unit.
    UNITS = {
        "1": ("Kilometres → Miles", lambda v: v * 0.621371, "mi"),
        "2": ("Miles → Kilometres", lambda v: v / 0.621371, "km"),
        "3": ("Celsius → Fahrenheit", lambda v: v * 9 / 5 + 32, "°F"),
        "4": ("Fahrenheit → Celsius", lambda v: (v - 32) * 5 / 9, "°C"),
        "5": ("Kilograms → Pounds", lambda v: v * 2.20462, "lb"),
        "6": ("Pounds → Kilograms", lambda v: v / 2.20462, "kg"),
    }

    def run(self):
        # Starts an interactive conversion menu.
        while True:

            # Prints the unit converter heading.
            print(f"\n  {color(208)}{BOLD}▌ UNIT CONVERTER{RESET}")

            # Displays all available conversion options.
            for key, (name, _, _) in self.UNITS.items():
                print(f"   {color(220)}{key}{RESET}  {name}")

            # Displays the option to return to the previous menu.
            print(f"   {color(220)}0{RESET}  {DIM}Back{RESET}")

            # Reads the user's conversion selection.
            choice = ask(f"  {color(208)}pick ❯{RESET} ")

            # Returns to the main menu if the user chooses 0 or q.
            if choice in ("0", "q", "back"):
                break

            # Checks whether the selected conversion exists.
            if choice not in self.UNITS:
                print(f"  {color(196)}✖ Choose 0-6{RESET}")
                continue

            # Retrieves the conversion name, function and output unit.
            name, fn, unit = self.UNITS[choice]

            # Requests the numeric value from the user.
            raw = ask(f"  {DIM}{name.split(' → ')[0]}:{RESET} ")

            try:
                # Converts the input to float, performs conversion and prints result.
                print(f"  {BOLD}{color(46)}= {fn(float(raw)):.2f} {unit}{RESET}")

            # Handles invalid numeric input.
            except ValueError:
                print(f"  {color(196)}✖ Please enter a number{RESET}")


# --------------------------------------------------------------------------
# MAIN APPLICATION
# Runs when the Python file is executed directly.
# --------------------------------------------------------------------------

def main():
    # Creates a Calculator object.
    calc = Calculator()

    # Displays the application banner.
    banner("BlazeOne", "Smart Calculator & Unit Converter")

    # Keeps displaying the main menu until the user exits.
    while True:

        # Displays all main application options.
        print(
            f"\n   {color(220)}1{RESET}  Calculator"
            f"\n   {color(220)}2{RESET}  Unit converter"
            f"\n   {color(220)}3{RESET}  About this module"
            f"\n   {color(220)}0{RESET}  {DIM}Exit{RESET}"
        )

        # Reads the user's menu selection.
        choice = ask(f"\n  {color(202)}blazeone ❯{RESET} ")

        # Opens the calculator if option 1 is selected.
        if choice == "1":
            calc.run()

        # Opens the unit converter if option 2 is selected.
        elif choice == "2":
            UnitConverter().run()

        # Displays information about reusable module components.
        elif choice == "3":
            print(
                f"\n  {DIM}Importable components:{RESET} "
                f"{BOLD}{', '.join(__all__)}{RESET}"
                f"\n  {DIM}Try:{RESET} from blazeone import banner, Calculator"
            )

        # Exits the application if the user selects 0 or q.
        elif choice in ("0", "q", "exit"):
            print(
                "\n  " +
                gradient_text("Thanks for using BlazeOne. Stay blazing!") +
                "\n"
            )
            break

        # Handles an invalid menu selection.
        else:
            print(f"  {color(196)}✖ Choose 0-3{RESET}")


# --------------------------------------------------------------------------
# MODULE EXECUTION CONTROL
# --------------------------------------------------------------------------

# Python sets __name__ to "__main__" when this file is executed directly.
# When imported by another file, Python sets __name__ to "blazeone".
# Therefore, main() runs only during direct execution, not during import.

if __name__ == "__main__":
    main()  # Starts the standalone BlazeOne application.
