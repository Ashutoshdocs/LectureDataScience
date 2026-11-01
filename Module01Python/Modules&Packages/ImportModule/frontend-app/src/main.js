// ⭐ The important line: importing the BlazeCalc module from the other folder.
// "blazecalc" resolves to ../BlazeCalc because of the "file:../BlazeCalc"
// dependency in package.json.
import BlazeCalc from "blazecalc";

// You can also use named imports:
// import { add, evaluate, Calculator } from "blazecalc";

const display = document.getElementById("display");
const keys = document.getElementById("keys");
const historyList = document.getElementById("history");
const errorBox = document.getElementById("error");

document.getElementById("version").textContent = `v${BlazeCalc.version}`;

// Keep a Calculator instance just to record history.
const calc = new BlazeCalc.Calculator();

const BUTTONS = [
  "7", "8", "9", "/",
  "4", "5", "6", "*",
  "1", "2", "3", "-",
  "0", ".", "C", "+",
  "=",
];

BUTTONS.forEach((label) => {
  const btn = document.createElement("button");
  btn.textContent = label;
  btn.className = label === "=" ? "equals" : /[+\-*/]/.test(label) ? "op" : "";
  btn.addEventListener("click", () => handleKey(label));
  keys.appendChild(btn);
});

display.addEventListener("keydown", (e) => {
  if (e.key === "Enter") handleKey("=");
});

function handleKey(key) {
  errorBox.textContent = "";
  if (key === "C") {
    display.value = "";
    return;
  }
  if (key === "=") {
    calculate();
    return;
  }
  display.value += key;
  display.focus();
}

function calculate() {
  const expression = display.value.trim();
  if (!expression) return;
  try {
    // 👇 Using BlazeCalc to do the actual work
    const result = BlazeCalc.evaluate(expression);
    calc.history.push(`${expression} = ${result}`);
    display.value = String(result);
    renderHistory();
  } catch (err) {
    errorBox.textContent = err.message;
  }
}

function renderHistory() {
  historyList.innerHTML = "";
  calc
    .getHistory()
    .slice()
    .reverse()
    .forEach((line) => {
      const li = document.createElement("li");
      li.textContent = line;
      historyList.appendChild(li);
    });
}
