"""BlazeCalc — public entry point.

Whatever is imported here is what other apps get when they write:

    import BlazeCalc
    from BlazeCalc import add, evaluate, Calculator
"""

from .operations import add, subtract, multiply, divide, percent, power, sqrt
from .calculator import Calculator, evaluate

__version__ = "1.0.0"

# __all__ controls what `from BlazeCalc import *` brings in
__all__ = [
    "add", "subtract", "multiply", "divide", "percent", "power", "sqrt",
    "Calculator", "evaluate", "__version__",
]
