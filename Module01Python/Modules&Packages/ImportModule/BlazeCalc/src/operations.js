// Basic math operations. Each one validates its inputs first.

function assertNumbers(...values) {
  for (const v of values) {
    if (typeof v !== "number" || Number.isNaN(v)) {
      throw new TypeError(`BlazeCalc: expected a number, got "${v}"`);
    }
  }
}

export function add(a, b) {
  assertNumbers(a, b);
  return a + b;
}

export function subtract(a, b) {
  assertNumbers(a, b);
  return a - b;
}

export function multiply(a, b) {
  assertNumbers(a, b);
  return a * b;
}

export function divide(a, b) {
  assertNumbers(a, b);
  if (b === 0) throw new RangeError("BlazeCalc: cannot divide by zero");
  return a / b;
}

export function percent(value, pct) {
  assertNumbers(value, pct);
  return (value * pct) / 100;
}

export function power(base, exponent) {
  assertNumbers(base, exponent);
  return base ** exponent;
}
