import { test } from "node:test";
import assert from "node:assert/strict";
import BlazeCalc, { add, divide, Calculator, evaluate } from "../src/index.js";

test("basic operations", () => {
  assert.equal(add(2, 3), 5);
  assert.equal(BlazeCalc.multiply(4, 5), 20);
  assert.equal(BlazeCalc.percent(200, 15), 30);
  assert.throws(() => divide(1, 0), RangeError);
});

test("Calculator class chains and records history", () => {
  const calc = new Calculator(10).apply("+", 5).apply("*", 2);
  assert.equal(calc.value, 30);
  assert.deepEqual(calc.getHistory(), ["10 + 5 = 15", "15 * 2 = 30"]);
});

test("evaluate respects operator precedence", () => {
  assert.equal(evaluate("12 + 3 * 4"), 24);
  assert.equal(evaluate("10 / 4 - 1"), 1.5);
});
