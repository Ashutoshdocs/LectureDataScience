# 🔥 BlazeCalc Demo — Using a Module from Another Folder

This demo teaches you how to **build a reusable JavaScript module in one folder** and **import it into a frontend app in another folder**.

```
blazecalc-demo/
├── BlazeCalc/              ← Folder 1: the calculator MODULE (the library)
│   ├── package.json        ← gives the module its name: "blazecalc"
│   ├── src/
│   │   ├── index.js        ← entry point: decides what gets exported
│   │   ├── operations.js   ← add, subtract, multiply, divide, percent, power
│   │   └── Calculator.js   ← Calculator class + evaluate("12 + 3 * 4")
│   └── test/
│       └── blazecalc.test.js
│
└── frontend-app/           ← Folder 2: the FRONTEND that USES the module
    ├── package.json        ← depends on "blazecalc": "file:../BlazeCalc"
    ├── index.html
    └── src/
        ├── main.js         ← import BlazeCalc from "blazecalc";
        └── style.css
```

---

## 🚀 Quick start

You need **Node.js 18+**.

```bash
# 1. (optional) test the module on its own
cd BlazeCalc
npm test

# 2. run the frontend app
cd ../frontend-app
npm install        # this links ../BlazeCalc into node_modules/blazecalc
npm run dev        # open the URL shown (usually http://localhost:5173)
```

Type `12 + 3 * 4` and press `=` → you get `24`. The UI is in `frontend-app`, but **all the math is done by BlazeCalc**.

---

## 📚 How it works — step by step

### Step 1 — Write the module (`BlazeCalc/src/operations.js`)

Plain functions, each one `export`ed so other files can use them:

```js
export function add(a, b) {
  return a + b;
}

export function divide(a, b) {
  if (b === 0) throw new RangeError("BlazeCalc: cannot divide by zero");
  return a / b;
}
```

### Step 2 — Create one entry point (`BlazeCalc/src/index.js`)

An entry point is the "front door" of your module. Users import from here, never from internal files.

```js
import * as operations from "./operations.js";
import { Calculator, evaluate } from "./Calculator.js";

// Named exports
export * from "./operations.js";
export { Calculator, evaluate };

// Default export — one object called BlazeCalc
const BlazeCalc = { ...operations, Calculator, evaluate, version: "1.0.0" };
export default BlazeCalc;
```

### Step 3 — Give the module a name (`BlazeCalc/package.json`)

```json
{
  "name": "blazecalc",
  "type": "module",
  "main": "./src/index.js",
  "exports": { ".": "./src/index.js" }
}
```

| Field | Meaning |
|---|---|
| `name` | The name other apps use to import it: `"blazecalc"` (npm names must be lowercase) |
| `type: "module"` | Use modern `import` / `export` syntax (ES Modules) |
| `main` / `exports` | Which file opens when someone writes `import ... from "blazecalc"` |

### Step 4 — Link the module into the frontend (`frontend-app/package.json`)

```json
"dependencies": {
  "blazecalc": "file:../BlazeCalc"
}
```

`file:../BlazeCalc` tells npm: *"this package isn't on the internet — it's in the folder next door."*
When you run `npm install`, npm creates a **symlink**:

```
frontend-app/node_modules/blazecalc  →  ../../BlazeCalc
```

Because it's a link (not a copy), **any change you make in `BlazeCalc/` shows up in the frontend immediately**.

### Step 5 — Import and use it (`frontend-app/src/main.js`)

```js
import BlazeCalc from "blazecalc";

BlazeCalc.add(2, 3);                  // 5
BlazeCalc.evaluate("12 + 3 * 4");     // 24
const calc = new BlazeCalc.Calculator();
```

Or pick only what you need with **named imports**:

```js
import { add, evaluate, Calculator } from "blazecalc";
```

### Step 6 — Run it

`npm run dev` starts **Vite**, a dev server that understands `import ... from "blazecalc"`, finds it in `node_modules`, and serves it to the browser.

---

## 🧰 BlazeCalc API reference

| Function | Example | Result |
|---|---|---|
| `add(a, b)` | `add(2, 3)` | `5` |
| `subtract(a, b)` | `subtract(9, 4)` | `5` |
| `multiply(a, b)` | `multiply(4, 5)` | `20` |
| `divide(a, b)` | `divide(10, 4)` | `2.5` (throws on `÷ 0`) |
| `percent(value, pct)` | `percent(200, 15)` | `30` |
| `power(base, exp)` | `power(2, 8)` | `256` |
| `evaluate(expr)` | `evaluate("12 + 3 * 4")` | `24` (respects × ÷ before + −, no `eval`) |
| `new Calculator(start)` | `new Calculator(10).apply("+", 5).apply("*", 2).value` | `30` |
| `calc.getHistory()` | | `["10 + 5 = 15", "15 * 2 = 30"]` |
| `calc.clear()` | | resets value and history |

All functions throw a `TypeError` if you pass something that isn't a number.

---

## 🏋️ Try it yourself (exercises)

1. **Add a new function.** Add `sqrt(n)` to `BlazeCalc/src/operations.js`. Because `index.js` uses `export *`, it's exported automatically. Use it in `main.js` — no reinstall needed thanks to the symlink.
2. **Add a `%` button** in the frontend that calls `BlazeCalc.percent()`.
3. **Write a test** for `power()` in `BlazeCalc/test/blazecalc.test.js` and run `npm test`.
4. **Use it from plain Node** (no browser):
   ```bash
   cd frontend-app
   node -e "import('blazecalc').then(m => console.log(m.default.evaluate('2 + 2 * 10')))"
   ```

---

## ❓ Common problems

| Problem | Fix |
|---|---|
| `Failed to resolve import "blazecalc"` | Run `npm install` inside `frontend-app/` |
| `Cannot use import statement outside a module` | Make sure `"type": "module"` is in `package.json` |
| Moved the folders and it broke | The path in `"file:../BlazeCalc"` is relative — update it and run `npm install` again |
| Opening `index.html` by double-click shows nothing | Browsers can't resolve `"blazecalc"` on their own — use `npm run dev` |

---

## 🌍 Going further

The same module can be shared in other ways once you outgrow `file:`:

- **npm workspaces** — put both folders under one root `package.json` with `"workspaces": ["BlazeCalc", "frontend-app"]`.
- **Publish to npm** — `cd BlazeCalc && npm publish`, then anyone can `npm install blazecalc` (you'd need a unique name).
- **Git dependency** — `"blazecalc": "github:your-user/BlazeCalc"`.

The import line in your app — `import BlazeCalc from "blazecalc"` — **stays exactly the same** in every case. That's the power of modules.
