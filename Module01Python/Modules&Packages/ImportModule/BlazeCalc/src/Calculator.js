// A stateful calculator class: keeps a running value and a history.
import { add, subtract, multiply, divide } from "./operations.js";

const OPERATORS = {
  "+": add,
  "-": subtract,
  "*": multiply,
  "/": divide,
};

export class Calculator {
  constructor(initial = 0) {
    this.value = initial;
    this.history = [];
  }

  // Apply an operator ("+", "-", "*", "/") with a number to the current value.
  apply(operator, number) {
    const fn = OPERATORS[operator];
    if (!fn) throw new Error(`BlazeCalc: unknown operator "${operator}"`);
    const result = fn(this.value, number);
    this.history.push(`${this.value} ${operator} ${number} = ${result}`);
    this.value = result;
    return this; // returning `this` allows chaining: calc.apply("+", 2).apply("*", 3)
  }

  clear() {
    this.value = 0;
    this.history = [];
    return this;
  }

  getHistory() {
    return [...this.history];
  }
}

// Evaluate a simple expression string like "12 + 3 * 4" safely
// (no eval). Respects * and / before + and -.
export function evaluate(expression) {
  const tokens = String(expression).match(/\d+(\.\d+)?|[+\-*/]/g);
  if (!tokens) throw new Error("BlazeCalc: empty expression");

  // Pass 1: handle * and /
  const stack = [Number(tokens[0])];
  for (let i = 1; i < tokens.length; i += 2) {
    const op = tokens[i];
    const num = Number(tokens[i + 1]);
    if (Number.isNaN(num)) throw new Error("BlazeCalc: invalid expression");
    if (op === "*" || op === "/") {
      stack.push(OPERATORS[op](stack.pop(), num));
    } else {
      stack.push(op, num);
    }
  }

  // Pass 2: handle + and -
  let result = stack[0];
  for (let i = 1; i < stack.length; i += 2) {
    result = OPERATORS[stack[i]](result, stack[i + 1]);
  }
  return result;
}
