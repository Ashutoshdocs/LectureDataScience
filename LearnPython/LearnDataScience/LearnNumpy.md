# NumPy Environment Setup – Theory and Practical Guide

> **Course continuity:** This README is the next chapter after **Python Vectors: Complete Foundation to NumPy**.  
> In the previous course, we learned what vectors are, how to work with them using normal Python lists, and why NumPy makes numerical operations easier and faster.  
> In this chapter, we will prepare a proper Python environment, install NumPy, verify the installation, and understand the tools and concepts involved before writing NumPy programs.

---

## Learning Objectives

By the end of this chapter, students will be able to:

1. Explain what an environment means in Python.
2. Understand why Python packages are installed separately.
3. Differentiate Python, pip, NumPy, and a virtual environment.
4. Check whether Python and pip are installed.
5. Create and activate a virtual environment.
6. Install NumPy using pip.
7. Verify the NumPy installation.
8. Run NumPy programs from a terminal and from an IDE.
9. Understand package versions and dependency management.
10. Troubleshoot common NumPy installation problems.

---

# Part 1 – Theory: Understanding the Python Environment

## Chapter 1 – What Is a Python Environment?

A Python environment is the setup in which Python programs execute.

It includes:

- The Python interpreter.
- Installed Python packages and libraries.
- Environment-specific configuration.
- The project files and code.
- Sometimes tools such as Jupyter Notebook or an IDE.

Think of Python as the engine that runs your program. Packages such as NumPy provide additional capabilities that the basic Python installation may not include.

### Simple example

Suppose we want to calculate the average of five numbers.

Using core Python:

```python
marks = [70, 80, 90, 60, 100]

average = sum(marks) / len(marks)

print(average)
```

For more advanced numerical work, we may want NumPy:

```python
import numpy as np

marks = np.array([70, 80, 90, 60, 100])

print(np.mean(marks))
```

The Python interpreter executes both programs. The second program additionally requires the NumPy package to be installed in the environment used to run the program.

### Important distinction

| Term | Meaning |
|---|---|
| Python | Programming language and its interpreter/runtime |
| pip | Tool used to install and manage Python packages |
| Package/library | Reusable code that provides additional functionality |
| NumPy | Python package for numerical computing and arrays |
| Environment | The Python interpreter and packages available to a project |
| Virtual environment | An isolated Python environment for a project |
| IDE/editor | Software used to write and manage code, such as VS Code or PyCharm |

---

## Chapter 2 – Why Do We Need NumPy?

Python already provides lists, tuples, loops, and mathematical functions. Why install NumPy?

NumPy is designed for numerical computing. It provides an efficient multidimensional array object and operations that work across arrays.

### Example: Python list

```python
numbers = [10, 20, 30]

# A list can store multiple values.
print(numbers)
```

### Example: NumPy array

```python
import numpy as np

numbers = np.array([10, 20, 30])

# A NumPy array is designed for numerical operations.
print(numbers)
```

### Why NumPy is useful

1. **Array operations:** Perform calculations on complete arrays without writing an explicit loop for every operation.
2. **Numerical functions:** Use functions for mean, median, standard deviation, minimum, maximum, and more.
3. **Multidimensional data:** Work with one-dimensional, two-dimensional, and higher-dimensional arrays.
4. **Performance:** NumPy operations are implemented using optimized low-level code and are often faster for large numerical workloads.
5. **Ecosystem:** Many data science and machine learning libraries work with NumPy arrays or integrate with NumPy.

### Important clarification

NumPy is not a replacement for every Python data structure. Use a normal list when it is suitable for general-purpose collections. Use NumPy arrays when you need numerical array operations.

---

## Chapter 3 – What Is a Python Package?

A package is reusable code that someone has developed so that other programmers do not need to implement the same functionality from scratch.

For example:

| Package | Common purpose |
|---|---|
| NumPy | Numerical arrays and mathematical operations |
| pandas | Tabular data analysis |
| Matplotlib | Data visualization |
| scikit-learn | Machine learning |
| requests | Making HTTP requests |

A package must be available in the Python environment used to run your program.

### What happens when we write an import?

```python
import numpy
```

Python searches the active interpreter's import paths for a package named `numpy`.

If it finds the package, the import succeeds. If it cannot find it, Python raises an error such as:

```text
ModuleNotFoundError: No module named 'numpy'
```

This usually means NumPy is not installed in the environment currently running the program, or the program is using a different interpreter from the one where NumPy was installed.

---

## Chapter 4 – What Is pip?

`pip` is Python's package installer. It downloads and installs packages from package indexes such as the Python Package Index (PyPI), subject to the configured package sources.

For example:

```bash
python -m pip install numpy
```

This command asks the selected Python interpreter to run its pip module and install NumPy.

### Why use `python -m pip` instead of only `pip`?

A computer can have more than one Python installation. The `pip` command may point to a different Python installation from the one used to run your script.

Using:

```bash
python -m pip install numpy
```

helps ensure that pip belongs to the Python interpreter selected by `python`.

On Windows, if the `python` command is not available but the Python launcher is installed, use:

```powershell
py -m pip install numpy
```

### Useful pip commands

```bash
# Display pip version and the Python installation it belongs to
python -m pip --version

# Install NumPy
python -m pip install numpy

# Display installed NumPy package information
python -m pip show numpy

# List installed packages
python -m pip list

# Upgrade NumPy
python -m pip install --upgrade numpy

# Uninstall NumPy
python -m pip uninstall numpy
```

Do not upgrade or uninstall packages in a shared or production environment without checking project requirements first.

---

## Chapter 5 – What Is a Virtual Environment?

A virtual environment is an isolated Python environment created for a particular project.

It allows different projects to use different package versions without unnecessarily affecting one another.

### Example problem without virtual environments

Imagine two projects:

- Project A requires NumPy version 1.x.
- Project B has been tested with NumPy version 2.x.

If both projects use the same global Python environment, changing the NumPy version for one project may affect the other project.

### Solution: Create separate virtual environments

```text
Python installation
│
├── Project A
│   └── .venv
│       └── NumPy version required by Project A
│
└── Project B
    └── .venv
        └── NumPy version required by Project B
```

Each project can manage its own installed packages.

### Benefits

- Reduces dependency conflicts between projects.
- Keeps project dependencies separate.
- Makes project setup easier to reproduce.
- Avoids installing every project package globally.
- Helps keep development environments organized.

### Important note

A virtual environment does not install a completely separate operating system or a separate copy of every system component. It creates an isolated Python environment that uses a base Python installation.

---

# Part 2 – Practical: Prepare the Environment

## Chapter 6 – Check Whether Python Is Installed

Before installing NumPy, confirm that Python is available.

### Windows PowerShell

```powershell
python --version
```

If that does not work, try:

```powershell
py --version
```

### Linux / Ubuntu

```bash
python3 --version
```

### Expected output

The exact version depends on the Python installation. For example:

```text
Python 3.x.x
```

The `x` characters represent version numbers. Do not expect every machine to show the same version.

### Check which Python executable is being used

Windows:

```powershell
where.exe python
```

Linux:

```bash
which python3
```

This is useful when multiple Python installations exist.

---

## Chapter 7 – Check pip

### Windows

```powershell
python -m pip --version
```

Or:

```powershell
py -m pip --version
```

### Linux / Ubuntu

```bash
python3 -m pip --version
```

If pip is unavailable, the method to install it depends on how Python was installed and on the operating system.

On Ubuntu, one possible package-manager approach is:

```bash
sudo apt update
sudo apt install python3-pip python3-venv
```

Use the operating system's package manager for system-level Python components. Avoid using `sudo pip install` to modify the operating system's managed Python environment.

---

## Chapter 8 – Create a Project Folder

Create a separate folder for the NumPy practical.

### Windows PowerShell

```powershell
mkdir numpy-learning
cd numpy-learning
```

### Linux / Ubuntu

```bash
mkdir numpy-learning
cd numpy-learning
```

The folder will hold the virtual environment and our Python files.

Recommended project structure:

```text
numpy-learning/
│
├── .venv/
│
├── 01_environment_check.py
├── 02_numpy_import.py
├── 03_numpy_version.py
├── 04_first_array.py
│
└── requirements.txt
```

The `.venv` directory is created in the next chapter. It should generally not be committed to Git because it is specific to a local environment.

---

## Chapter 9 – Create a Virtual Environment

Run this command from inside the `numpy-learning` folder.

### Windows PowerShell

```powershell
python -m venv .venv
```

If using the Python launcher:

```powershell
py -m venv .venv
```

### Linux / Ubuntu

```bash
python3 -m venv .venv
```

### What does this command mean?

| Part | Explanation |
|---|---|
| `python` / `python3` | Runs the Python interpreter |
| `-m` | Runs a Python module as a command |
| `venv` | Python's built-in virtual environment module |
| `.venv` | Name of the folder where the environment is created |

The command creates the virtual environment. It does not install NumPy.

---

## Chapter 10 – Activate the Virtual Environment

Creating a virtual environment and activating it are two different steps.

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, the terminal prompt commonly displays:

```text
(.venv) PS C:\...\numpy-learning>
```

#### If PowerShell blocks the activation script

You may see an execution-policy error. One option for the current PowerShell process is:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

This changes the policy only for the current PowerShell process. Follow your organization's security policy on managed machines.

You can also use Command Prompt activation:

```cmd
.venv\Scripts\activate.bat
```

### Linux / Ubuntu

```bash
source .venv/bin/activate
```

The prompt commonly displays:

```text
(.venv) user@machine:~/numpy-learning$
```

### How do we know activation worked?

Run:

```bash
python --version
```

Then check the Python executable path.

Windows:

```powershell
where.exe python
```

Linux:

```bash
which python
```

The selected Python path should point inside the project's `.venv` directory.

### Deactivate the environment

When you finish working:

```bash
deactivate
```

This exits the virtual environment in the current terminal session.

---

## Chapter 11 – Install NumPy Inside the Virtual Environment

Make sure the virtual environment is active before installing NumPy.

Run:

```bash
python -m pip install numpy
```

pip will install NumPy and any required package files into the active environment.

### Verify the installation

```bash
python -m pip show numpy
```

You should see package information such as:

- Name
- Version
- Installation location

The installation location should be associated with the project's `.venv` environment.

### Verify with pip list

```bash
python -m pip list
```

NumPy should appear in the package list.

### Important

Installing NumPy globally and installing NumPy inside `.venv` are not necessarily the same thing. Always check which Python interpreter is active.

---

# Part 3 – Verify NumPy with Python Programs

## Chapter 12 – Program 1: Check the Python Environment

Create a file named `01_environment_check.py`.

```python
# Import the sys module.
# It provides information about the Python interpreter.
import sys

# Display the Python version.
print("Python version:")
print(sys.version)

# Display the executable path of the Python interpreter.
# This helps us identify which environment is running the program.
print("\nPython executable:")
print(sys.executable)
```

Run it:

```bash
python 01_environment_check.py
```

### What should students observe?

- The Python version.
- The path of the interpreter.
- Whether the interpreter path points inside `.venv`.

The executable path is especially useful when troubleshooting package installation issues.

---

## Chapter 13 – Program 2: Import NumPy

Create `02_numpy_import.py`.

```python
# Import NumPy.
# The alias np is the widely used convention in Python examples.
import numpy as np

# Display a message to confirm that the import succeeded.
print("NumPy imported successfully!")

# Display the NumPy version installed in this environment.
print("NumPy version:", np.__version__)
```

Run:

```bash
python 02_numpy_import.py
```

### Expected result

The program should print a success message and the installed NumPy version.

The version number may be different on different computers.

### What if the import fails?

If you see:

```text
ModuleNotFoundError: No module named 'numpy'
```

Check these items:

1. Is the virtual environment activated?
2. Did you install NumPy after activating it?
3. Is the same Python interpreter being used to run the script?
4. Does `python -m pip show numpy` display NumPy?
5. Does `sys.executable` point to the expected `.venv` folder?

---

## Chapter 14 – Program 3: Create Your First NumPy Array

Create `04_first_array.py`.

```python
# Import NumPy using the standard alias.
import numpy as np

# Create a NumPy array from a Python list.
numbers = np.array([10, 20, 30, 40, 50])

# Display the array.
print("Array:", numbers)

# Display the data type of the array.
print("Data type:", numbers.dtype)

# Display the number of dimensions.
print("Dimensions:", numbers.ndim)

# Display the shape of the array.
print("Shape:", numbers.shape)

# Display the total number of elements.
print("Size:", numbers.size)
```

### Understand the output

For this one-dimensional array:

- `dtype` tells us the element data type selected by NumPy.
- `ndim` tells us the number of dimensions.
- `shape` tells us the size along each dimension.
- `size` tells us the total number of elements.

The exact `dtype` can depend on the values and platform.

---

# Part 4 – Understand How the Environment Works

## Chapter 15 – Global Python vs Virtual Environment

| Feature | Global Python environment | Project virtual environment |
|---|---|---|
| Scope | Shared by projects using that installation | Intended for one project |
| Package installation | May affect other projects | Isolated from other project environments |
| Dependency management | Can become difficult as projects grow | Easier to manage per project |
| Recommended use | System tools and carefully managed shared use | Most application and learning projects |

### Demonstration

1. Deactivate the virtual environment.
2. Run `python -m pip show numpy`.
3. Activate `.venv`.
4. Run `python -m pip show numpy` again.

The results may differ because the two commands can use different Python environments.

Do not assume NumPy must be installed globally just because it is installed in `.venv`.

---

## Chapter 16 – What Is requirements.txt?

A project often needs more than one package. We need a way to record the packages and versions used by the project.

A `requirements.txt` file is a common way to list Python dependencies.

### Generate requirements.txt

With the virtual environment active:

```bash
python -m pip freeze > requirements.txt
```

This records installed packages and their versions in the current environment.

A simple file might contain an entry such as:

```text
numpy==<installed-version>
```

The actual version will be written by pip; do not type the placeholder literally.

### Install packages from requirements.txt

On another machine, after creating and activating a virtual environment:

```bash
python -m pip install -r requirements.txt
```

### Why is this useful?

Suppose a student or teammate wants to run the same project. Instead of manually installing every package, they can install the listed dependencies with one command.

### Best practice

For a small teaching project, keep the requirements file focused on the dependencies the project needs. `pip freeze` records all installed packages in the environment, which may include packages that are not direct project requirements.

---

## Chapter 17 – Select the Correct Interpreter in VS Code

Installing NumPy in a terminal does not guarantee that VS Code is using the same Python interpreter.

### Steps

1. Open the `numpy-learning` folder in VS Code.
2. Ensure the Python extension is installed.
3. Open the Command Palette.
4. Search for **Python: Select Interpreter**.
5. Select the interpreter inside the project's `.venv` folder.
6. Open a new terminal in VS Code.
7. Confirm that the terminal is using the expected environment.
8. Run the NumPy program.

Typical interpreter paths:

Windows:

```text
numpy-learning\.venv\Scripts\python.exe
```

Linux:

```text
numpy-learning/.venv/bin/python
```

### Verify from VS Code

Run this in the VS Code terminal:

```bash
python -c "import sys; print(sys.executable)"
```

Then:

```bash
python -c "import numpy as np; print(np.__version__)"
```

If both commands work, the selected interpreter can import NumPy.

---

## Chapter 18 – Using NumPy in Jupyter Notebook

Jupyter Notebook is an interactive environment where Python code is written and executed in cells.

It is useful for data analysis, experimentation, and teaching.

### Install Jupyter in the virtual environment

```bash
python -m pip install notebook
```

Launch it:

```bash
jupyter notebook
```

If the command is not found, you can try:

```bash
python -m notebook
```

In a notebook cell, run:

```python
import numpy as np

numbers = np.array([10, 20, 30, 40, 50])

print(numbers)
print(np.mean(numbers))
```

### Important concept: Kernel

A Jupyter kernel is the process that executes notebook code.

The notebook interface and the kernel are not the same thing. A notebook may be open in a browser while its kernel uses a different Python environment.

If NumPy is installed in `.venv` but the notebook uses another kernel, the import may fail.

For a project-specific kernel, install `ipykernel` in the virtual environment:

```bash
python -m pip install ipykernel
```

Register it:

```bash
python -m ipykernel install --user --name numpy-learning --display-name "Python (numpy-learning)"
```

Then select **Python (numpy-learning)** as the notebook kernel.

---

# Part 5 – Common Errors and Troubleshooting

## Chapter 19 – Common Problems

### Problem 1: `python` is not recognized

Possible reason:
- Python is not installed, or its executable is not available through PATH.

Try on Windows:

```powershell
py --version
```

If Python is installed, the Python launcher may work even when `python` does not.

### Problem 2: `No module named 'numpy'`

Possible reason:
- NumPy is not installed in the interpreter running the program.

Check:

```bash
python -m pip show numpy
python -c "import sys; print(sys.executable)"
```

Install using the same interpreter:

```bash
python -m pip install numpy
```

### Problem 3: NumPy installed but VS Code shows an import error

Possible reason:
- VS Code selected a different interpreter.

Solution:
- Use **Python: Select Interpreter**.
- Select the project's `.venv` interpreter.
- Run the verification commands again.

### Problem 4: PowerShell does not allow activation

Possible reason:
- PowerShell's execution policy blocks the activation script.

For the current PowerShell process, you can use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then:

```powershell
.\.venv\Scripts\Activate.ps1
```

Use this only where permitted by your device or organization's security policy.

### Problem 5: `pip` is not recognized

Use pip through Python:

```bash
python -m pip --version
```

Then install:

```bash
python -m pip install numpy
```

### Problem 6: Permission denied during installation

Possible reason:
- You are trying to install into a protected system Python environment.

Recommended approach:
- Create a virtual environment in your project folder.
- Activate it.
- Install NumPy inside it.

Avoid using `sudo pip install` as a general fix.

### Problem 7: `externally-managed-environment` on Ubuntu

Some Linux distributions protect their system-managed Python installation.

Recommended approach:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install numpy
```

If virtual environment creation fails because the venv package is missing, install the appropriate OS package, for example:

```bash
sudo apt update
sudo apt install python3-venv
```

---

# Part 6 – Student Practice

## Chapter 20 – Practical Exercises

### Exercise 1 – Environment inspection

1. Check the Python version.
2. Check the pip version.
3. Display the Python executable path.
4. Explain why the executable path matters.

### Exercise 2 – Create a virtual environment

1. Create a folder named `numpy-practice`.
2. Create a virtual environment named `.venv`.
3. Activate it.
4. Confirm that the terminal prompt shows the environment name.
5. Deactivate it.

### Exercise 3 – Install NumPy

1. Activate the environment.
2. Install NumPy.
3. Check the installed version.
4. Display NumPy package information.
5. Import NumPy from a Python file.

### Exercise 4 – Interpreter mismatch

1. Install NumPy in `.venv`.
2. Deactivate `.venv`.
3. Check whether the global interpreter can import NumPy.
4. Activate `.venv` again.
5. Compare the results.
6. Explain why the results may differ.

### Exercise 5 – Dependency file

1. Install NumPy.
2. Create `requirements.txt`.
3. Read the file.
4. Create a second virtual environment.
5. Install dependencies from `requirements.txt`.
6. Verify that NumPy imports successfully.

### Exercise 6 – VS Code

1. Open the project folder in VS Code.
2. Select the `.venv` interpreter.
3. Run a Python file that imports NumPy.
4. Print `sys.executable`.
5. Explain how you confirmed that VS Code used the correct environment.

---

# Part 7 – Quick Revision

## Chapter 21 – Important Commands Cheat Sheet

| Task | Windows PowerShell | Linux / Ubuntu |
|---|---|---|
| Check Python | `python --version` or `py --version` | `python3 --version` |
| Check pip | `python -m pip --version` | `python3 -m pip --version` |
| Create venv | `python -m venv .venv` | `python3 -m venv .venv` |
| Activate venv | `.\.venv\Scripts\Activate.ps1` | `source .venv/bin/activate` |
| Install NumPy | `python -m pip install numpy` | `python -m pip install numpy` |
| Check NumPy | `python -m pip show numpy` | `python -m pip show numpy` |
| List packages | `python -m pip list` | `python -m pip list` |
| Save dependencies | `python -m pip freeze > requirements.txt` | `python -m pip freeze > requirements.txt` |
| Install dependencies | `python -m pip install -r requirements.txt` | `python -m pip install -r requirements.txt` |
| Deactivate venv | `deactivate` | `deactivate` |

The commands in the install and pip rows assume the virtual environment is active and `python` points to that environment.

## Chapter 22 – Questions to Check Understanding

1. What is a Python environment?
2. What is the difference between Python and NumPy?
3. What is a Python package?
4. What is the purpose of pip?
5. Why do we use `python -m pip`?
6. What is a virtual environment?
7. Does creating a virtual environment install NumPy automatically?
8. What is the difference between creating and activating a virtual environment?
9. Why can one project use a different NumPy version from another project?
10. What does `sys.executable` display?
11. What is the purpose of `requirements.txt`?
12. What is the difference between a Jupyter notebook and its kernel?
13. Why might NumPy work in a terminal but fail in VS Code?
14. What does `ModuleNotFoundError` mean?
15. Why should we avoid installing packages into an OS-managed Python environment?

---

# Final Course Connection – What Comes Next?

In the previous course, we learned the mathematical idea of a vector and implemented vector operations using Python lists. We then introduced NumPy arrays and performed numerical operations.

In this chapter, we prepared the environment required to run NumPy programs reliably.

The next chapter can now focus on NumPy itself:

1. Creating arrays using `np.array()`.
2. Understanding array dimensions and shapes.
3. Creating arrays using `zeros()`, `ones()`, `arange()`, and `linspace()`.
4. Understanding array data types.
5. Performing vector arithmetic.
6. Indexing, slicing, filtering, and aggregation.
7. Applying NumPy to student marks and monthly sales projects.

**Teaching sequence:** First understand the environment, then install and verify the library, and only then begin learning NumPy array operations.
