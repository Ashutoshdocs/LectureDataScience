# LAB 1 — Python `math` Module

## Purpose
Mathematical functions and constants.

## What you will learn
Math functions help perform common calculations. `math` also provides constants such as `pi` and functions such as `sqrt()`, `ceil()`, `floor()`, `factorial()`, and `gcd()`.

## Code

```python
import math

print("Pi:", math.pi)
print("Square root of 81:", math.sqrt(81))
print("Power 2^5:", math.pow(2, 5))
print("Ceiling of 4.2:", math.ceil(4.2))
print("Floor of 4.8:", math.floor(4.8))
print("Factorial of 5:", math.factorial(5))
print("Greatest common divisor:", math.gcd(24, 36))

angle_degrees = 90
angle_radians = math.radians(angle_degrees)
print("Sine of 90 degrees:", math.sin(angle_radians))
```

## Run the lab

From this lab's folder:

```bash
python3 lab.py
```

On Windows, you can use:

```powershell
py lab.py
```

## Expected result
The script prints example values demonstrating the module. Some values are intentionally different on each run or machine (for example, random numbers, current date/time, paths, and platform information).

## Try it yourself
Change the values and calculate the square root, factorial, and GCD of different numbers. Note: `math.pow()` returns a float; `**` is Python's power operator.

## Key takeaway
This is a Python standard-library module. You can import it directly; no `pip install` is required.
