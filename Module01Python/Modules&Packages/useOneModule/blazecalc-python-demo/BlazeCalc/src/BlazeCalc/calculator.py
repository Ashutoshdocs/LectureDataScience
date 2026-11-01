"""A stateful Calculator class and a safe expression evaluator."""

import ast
import operator

from .operations import add, subtract, multiply, divide, power

_OPERATORS = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
    "**": power,
}


class Calculator:
    """Keeps a running value and a history of every step."""

    def __init__(self, initial=0):
        self.value = initial
        self.history = []

    def apply(self, op, number):
        if op not in _OPERATORS:
            raise ValueError(f"BlazeCalc: unknown operator {op!r}")
        result = _OPERATORS[op](self.value, number)
        self.history.append(f"{self.value} {op} {number} = {result}")
        self.value = result
        return self  # allows chaining: calc.apply("+", 2).apply("*", 3)

    def record(self, expression, result):
        """Store an already-evaluated expression in the history."""
        self.history.append(f"{expression} = {result}")

    def clear(self):
        self.value = 0
        self.history = []
        return self

    def get_history(self):
        return list(self.history)


# ---- Safe evaluate() --------------------------------------------------------
# We parse the text into a syntax tree and only allow numbers, + - * / ** %
# and parentheses. Python's eval() is NEVER used, so input like
# "__import__('os').remove('x')" is rejected.

_BIN_OPS = {
    ast.Add: add,
    ast.Sub: subtract,
    ast.Mult: multiply,
    ast.Div: divide,
    ast.Pow: power,
    ast.Mod: operator.mod,
}
_UNARY_OPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def _eval_node(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) \
            and not isinstance(node.value, bool):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BIN_OPS:
        left, right = _eval_node(node.left), _eval_node(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 1000:
            raise ValueError("BlazeCalc: exponent too large")
        return _BIN_OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        return _UNARY_OPS[type(node.op)](_eval_node(node.operand))
    raise ValueError("BlazeCalc: invalid expression")


def evaluate(expression):
    """Evaluate text like "12 + 3 * 4" or "(2 + 3) ** 2" safely."""
    text = str(expression).strip().replace("×", "*").replace("÷", "/")
    if not text:
        raise ValueError("BlazeCalc: empty expression")
    try:
        tree = ast.parse(text, mode="eval")
    except SyntaxError:
        raise ValueError("BlazeCalc: invalid expression") from None
    result = _eval_node(tree.body)
    # Show 6.0 as 6, and tidy floating point noise like 0.30000000000000004
    if isinstance(result, float):
        result = round(result, 10)
        if result.is_integer():
            result = int(result)
    return result
