// Public entry point of the BlazeCalc module.
// Everything exported here is what other apps can import.
import * as operations from "./operations.js";
import { Calculator, evaluate } from "./Calculator.js";

// Named exports:  import { add, Calculator } from "blazecalc";
export * from "./operations.js";
export { Calculator, evaluate };

// Default export: import BlazeCalc from "blazecalc";
const BlazeCalc = {
  ...operations,
  Calculator,
  evaluate,
  version: "1.0.0",
};

export default BlazeCalc;
