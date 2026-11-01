import unittest

import BlazeCalc
from BlazeCalc import add, divide, Calculator, evaluate


class TestOperations(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(BlazeCalc.multiply(4, 5), 20)
        self.assertEqual(BlazeCalc.percent(200, 15), 30)
        self.assertEqual(BlazeCalc.sqrt(81), 9)

    def test_errors(self):
        with self.assertRaises(ZeroDivisionError):
            divide(1, 0)
        with self.assertRaises(TypeError):
            add("2", 3)


class TestCalculator(unittest.TestCase):
    def test_chaining_and_history(self):
        calc = Calculator(10).apply("+", 5).apply("*", 2)
        self.assertEqual(calc.value, 30)
        self.assertEqual(calc.get_history(), ["10 + 5 = 15", "15 * 2 = 30"])


class TestEvaluate(unittest.TestCase):
    def test_precedence_and_parentheses(self):
        self.assertEqual(evaluate("12 + 3 * 4"), 24)
        self.assertEqual(evaluate("(2 + 3) ** 2"), 25)
        self.assertEqual(evaluate("10 / 4 - 1"), 1.5)
        self.assertEqual(evaluate("-5 + 2"), -3)
        self.assertEqual(evaluate("0.1 + 0.2"), 0.3)

    def test_rejects_unsafe_input(self):
        for bad in ["__import__('os')", "abc", "2 +", "", "9 ** 99999"]:
            with self.assertRaises(ValueError):
                evaluate(bad)


if __name__ == "__main__":
    unittest.main()
