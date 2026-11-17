# Python Virtual Environment (venv) – Complete Practical Guide

## 1. What is a Python Virtual Environment?

A Python Virtual Environment is an isolated Python workspace that allows us to install and manage Python packages separately for different projects.

Normally, Python packages can be installed globally on a machine. This means multiple projects may use the same installed packages.

This can create problems when different projects require different versions of the same package.

### Real-World Example

Imagine you are working on two projects:

| Project | Required Packages |
|---|---|
| Project 1 – Machine Learning | pandas, numpy, scikit-learn |
| Project 2 – Web Development | flask, requests |

Without virtual environments:

- All packages may be installed into the same Python environment.
- Projects can experience dependency conflicts.
- Updating a package for one project might break another project.
- Managing project dependencies becomes difficult.

With virtual environments:

- Every project gets its own isolated Python environment.
- Packages are installed separately.
- Different projects can use different versions of the same package.
- Removing one environment does not affect another.

**Important:** A virtual environment does not install a completely separate operating system or Python installation. It creates an isolated Python environment with its own package installation directory and executable references.

---

## 2. Understand the Practical Architecture

We will create two independent environments.

```text
Python-Virtual-Environment/
│
├── env1/
│   └── Python Environment 1
│       ├── requests
│       └── pandas
│
├── env2/
│   └── Python Environment 2
│       ├── flask
│       └── numpy
│
├── project1.py
├── project2.py
└── README.md
```

Expected package availability:

| Package | env1 | env2 |
|---|---|---|
| requests | Yes | No |
| pandas | Yes | No |
| flask | No | Yes |
| numpy | No | Yes |

We will verify this practically.

---

# PART 1 – Check Python Installation

## Step 1: Verify Python

Open your terminal.

### Windows PowerShell

```powershell
python --version
```

If that does not work:

```powershell
py --version
```

### Linux / Ubuntu

```bash
python3 --version
```

Check pip:

```bash
python -m pip --version
```

On Ubuntu:

```bash
python3 -m pip --version
```

## Step 2: Create the Project Directory

### Windows PowerShell

```powershell
mkdir Python-Virtual-Environment
cd Python-Virtual-Environment
```

### Linux / Ubuntu

```bash
mkdir Python-Virtual-Environment
cd Python-Virtual-Environment
```

---

# PART 2 – Create Environment 1

## Step 3: Create the First Virtual Environment

### Windows

```powershell
python -m venv env1
```

Or:

```powershell
py -m venv env1
```

### Linux / Ubuntu

```bash
python3 -m venv env1
```

If the venv module is missing on Ubuntu:

```bash
sudo apt update
sudo apt install python3-venv -y
```

Create the environment again:

```bash
python3 -m venv env1
```

### What happened?

Python created a directory named `env1`.

It contains:

- A Python executable or reference to the base Python installation.
- An isolated package installation directory.
- Activation scripts.
- Environment configuration.

## Step 4: Activate Environment 1

### Windows PowerShell

```powershell
.\env1\Scripts\Activate.ps1
```

If PowerShell blocks the activation script, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again:

```powershell
.\env1\Scripts\Activate.ps1
```

### Windows CMD

```cmd
env1\Scripts\activate.bat
```

### Linux / Ubuntu / macOS

```bash
source env1/bin/activate
```

### How do you know it is activated?

Your terminal will show something like:

```text
(env1) PS C:\Python-Virtual-Environment>
```

Or on Linux:

```text
(env1) user@ubuntu:~/Python-Virtual-Environment$
```

The `(env1)` prefix indicates that Environment 1 is active.

## Step 5: Verify the Active Python

```bash
python --version
```

Check the Python executable location:

### Windows

```powershell
where.exe python
```

### Linux / Ubuntu

```bash
which python
```

Expected locations:

```text
Windows:
Python-Virtual-Environment\env1\Scripts\python.exe

Linux:
Python-Virtual-Environment/env1/bin/python
```

This proves that your terminal is using Python from `env1`.

## Step 6: Install Packages in Environment 1

Install two packages:

```bash
python -m pip install requests pandas
```

Check installed packages:

```bash
python -m pip list
```

Check individual packages:

```bash
python -m pip show requests
python -m pip show pandas
```

Save installed dependencies:

```bash
python -m pip freeze > requirements-env1.txt
```

The file contains the installed package versions.

## Step 7: Create a Python Program for Environment 1

Create a file named `project1.py`.

```python
import requests
import pandas as pd

print("Welcome to Environment 1")

print("Requests Version:", requests.__version__)
print("Pandas Version:", pd.__version__)

data = {
    "Name": ["Amit", "Rahul", "Priya"],
    "Marks": [85, 90, 95]
}

df = pd.DataFrame(data)

print("\nStudent Data:")
print(df)
```

Execute:

```bash
python project1.py
```

Expected result:

```text
Welcome to Environment 1

Requests Version: ...
Pandas Version: ...

Student Data:
    Name  Marks
0   Amit     85
1  Rahul     90
2  Priya     95
```

**Observation:** Both requests and pandas work because they were installed in `env1`.

---

# PART 3 – Exit Environment 1

## Step 8: Deactivate Environment 1

Execute:

```bash
deactivate
```

What happens?

- The `(env1)` prefix disappears.
- Your terminal returns to the original Python environment.
- Your shell stops using the virtual environment's Python executable.
- The environment directory and its installed packages are NOT deleted.

Example:

Before:

```text
(env1) PS C:\Python-Virtual-Environment>
```

After:

```text
PS C:\Python-Virtual-Environment>
```

**Important:** Deactivate means exit the environment, not delete it.

---

# PART 4 – Create Environment 2

## Step 9: Create the Second Environment

Make sure you have deactivated `env1`.

### Windows

```powershell
python -m venv env2
```

### Linux / Ubuntu

```bash
python3 -m venv env2
```

We now have two separate environments:

```text
Python-Virtual-Environment/
│
├── env1/
└── env2/
```

## Step 10: Activate Environment 2

### Windows PowerShell

```powershell
.\env2\Scripts\Activate.ps1
```

### Linux / Ubuntu

```bash
source env2/bin/activate
```

Your terminal should now show:

```text
(env2)
```

## Step 11: Verify Python Location

### Windows

```powershell
where.exe python
```

### Linux

```bash
which python
```

Expected location:

```text
Python-Virtual-Environment/env2/...
```

This proves that you are now using Environment 2 instead of Environment 1.

## Step 12: Install Different Packages

Install Flask and NumPy:

```bash
python -m pip install flask numpy
```

Check installed packages:

```bash
python -m pip list
```

Save dependencies:

```bash
python -m pip freeze > requirements-env2.txt
```

## Step 13: Create a Program for Environment 2

Create `project2.py`.

```python
import flask
import numpy as np

print("Welcome to Environment 2")

print("Flask Version:", flask.__version__)
print("NumPy Version:", np.__version__)

numbers = np.array([10, 20, 30, 40, 50])

print("\nNumPy Array:")
print(numbers)

print("Average:", np.mean(numbers))
```

Note: For newer Flask versions, `flask.__version__` may generate a deprecation warning. You can alternatively use `importlib.metadata.version("flask")`.

Execute:

```bash
python project2.py
```

Expected result:

```text
Welcome to Environment 2

Flask Version: ...
NumPy Version: ...

NumPy Array:
[10 20 30 40 50]

Average: 30.0
```

**Observation:** Flask and NumPy work because they were installed in `env2`.

---

# PART 5 – PROVE THAT ENVIRONMENTS ARE ISOLATED

This is the most important part of the practical.

We will prove that packages installed in one environment are not automatically available in another.

## Experiment 1: Check Environment 2

While `env2` is active:

```bash
python -m pip list
```

You should see:

- flask
- numpy

Try importing requests:

```bash
python -c "import requests"
```

Expected:

```text
ModuleNotFoundError: No module named 'requests'
```

Try importing pandas:

```bash
python -c "import pandas"
```

Expected:

```text
ModuleNotFoundError: No module named 'pandas'
```

Why?

Because we installed requests and pandas in `env1`, not `env2`.

## Experiment 2: Switch Back to Environment 1

First deactivate:

```bash
deactivate
```

Activate `env1`:

### Windows

```powershell
.\env1\Scripts\Activate.ps1
```

### Linux

```bash
source env1/bin/activate
```

Check installed packages:

```bash
python -m pip list
```

Now execute:

```bash
python -c "import requests; print('Requests is working')"
```

Expected:

```text
Requests is working
```

Execute:

```bash
python -c "import pandas; print('Pandas is working')"
```

Expected:

```text
Pandas is working
```

Now try Flask:

```bash
python -c "import flask"
```

Expected:

```text
ModuleNotFoundError: No module named 'flask'
```

Try NumPy:

```bash
python -c "import numpy"
```

Expected:

```text
ModuleNotFoundError: No module named 'numpy'
```

## Experiment 3: Switch Between Both Environments

Repeat the following sequence.

```bash
deactivate
```

Activate Environment 2:

```bash
# Windows
.\env2\Scripts\Activate.ps1

# Linux
source env2/bin/activate
```

Check:

```bash
python -m pip list
```

Switch back:

```bash
deactivate
```

Activate Environment 1:

```bash
# Windows
.\env1\Scripts\Activate.ps1

# Linux
source env1/bin/activate
```

Check again:

```bash
python -m pip list
```

### Final Isolation Result

| Test | env1 | env2 |
|---|---|---|
| Import requests | Success | Failure |
| Import pandas | Success | Failure |
| Import flask | Failure | Success |
| Import numpy | Failure | Success |
| Run project1.py | Success | Missing dependencies |
| Run project2.py | Missing dependencies | Success |

The experiments prove that the two environments have independent package installations.

---

# PART 6 – Understand Activation and Deactivation

Students often get confused about what happens when we activate or deactivate an environment.

### Activate

```bash
source env1/bin/activate
```

Windows:

```powershell
.\env1\Scripts\Activate.ps1
```

The shell modifies its PATH so that the virtual environment's Python and pip executables are found first.

### Deactivate

```bash
deactivate
```

The shell restores its previous environment settings.

### Activate Again

```bash
source env1/bin/activate
```

The same environment becomes active again.

**Important:** Every time you open a new terminal, you generally need to activate your environment again.

Activation is a terminal-session operation. It does not permanently activate an environment for your entire machine.

---

# PART 7 – Remove and Clean Up Environments

Suppose Environment 1 is no longer required.

First, deactivate it if it is currently active:

```bash
deactivate
```

Now delete the environment directory.

### Windows PowerShell

```powershell
Remove-Item -Recurse -Force env1
```

### Linux / Ubuntu

```bash
rm -rf env1
```

Check the directory:

```bash
ls
```

On Windows:

```powershell
Get-ChildItem
```

You should now see:

```text
Python-Virtual-Environment/
│
├── env2/
├── project1.py
├── project2.py
├── requirements-env1.txt
└── requirements-env2.txt
```

Environment 1 is deleted, but Environment 2 is still available.

Activate Environment 2:

```bash
# Windows
.\env2\Scripts\Activate.ps1

# Linux
source env2/bin/activate
```

Check:

```bash
python -m pip list
```

Flask and NumPy are still installed.

**Important:** Deleting `env1` does not delete packages installed in `env2`.

To delete Environment 2 as well:

```bash
deactivate
```

Windows:

```powershell
Remove-Item -Recurse -Force env2
```

Linux:

```bash
rm -rf env2
```

Both virtual environments are now removed.

---

# PART 8 – Recreate an Environment Using requirements.txt

What if you delete an environment but want to recreate it later?

This is where `requirements.txt` becomes useful.

A requirements file stores the package dependencies and their versions.

For example:

```text
requests==...
pandas==...
```

The actual version numbers are generated by:

```bash
python -m pip freeze
```

## Recreate Environment 1

Create:

```bash
python -m venv env1
```

Activate:

```bash
# Windows
.\env1\Scripts\Activate.ps1

# Linux
source env1/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements-env1.txt
```

Verify:

```bash
python -m pip list
```

Your packages will be restored from the requirements file.

## Recreate Environment 2

```bash
python -m venv env2
```

Activate it and install:

```bash
# Windows
.\env2\Scripts\Activate.ps1

# Linux
source env2/bin/activate
```

```bash
python -m pip install -r requirements-env2.txt
```

Now both environments can be independently recreated.

---

# PART 9 – Important Commands Cheat Sheet

| Operation | Windows PowerShell | Linux / Ubuntu |
|---|---|---|
| Check Python | `python --version` | `python3 --version` |
| Create env1 | `python -m venv env1` | `python3 -m venv env1` |
| Create env2 | `python -m venv env2` | `python3 -m venv env2` |
| Activate env1 | `.\env1\Scripts\Activate.ps1` | `source env1/bin/activate` |
| Activate env2 | `.\env2\Scripts\Activate.ps1` | `source env2/bin/activate` |
| Deactivate | `deactivate` | `deactivate` |
| Install package | `python -m pip install pandas` | `python -m pip install pandas` |
| List packages | `python -m pip list` | `python -m pip list` |
| Show dependencies | `python -m pip freeze` | `python -m pip freeze` |
| Export dependencies | `python -m pip freeze > requirements.txt` | Same |
| Install dependencies | `python -m pip install -r requirements.txt` | Same |
| Delete environment | `Remove-Item -Recurse -Force env1` | `rm -rf env1` |

---

# PART 10 – Best Practices in Real Projects

## 1. One Environment Per Project

Recommended:

```text
Projects/
│
├── MachineLearning/
│   ├── .venv/
│   ├── requirements.txt
│   └── main.py
│
├── FlaskApplication/
│   ├── .venv/
│   ├── requirements.txt
│   └── app.py
│
└── DataAnalysis/
    ├── .venv/
    ├── requirements.txt
    └── analysis.py
```

Each project has its own environment.

## 2. Never Upload Your Virtual Environment to GitHub

Virtual environments contain many files and are machine-specific.

Add this to `.gitignore`:

```gitignore
.venv/
venv/
env/
env1/
env2/
__pycache__/
*.pyc
```

Upload your source code and requirements file instead.

## 3. Always Use python -m pip

Prefer:

```bash
python -m pip install pandas
```

Instead of:

```bash
pip install pandas
```

Why?

`python -m pip` explicitly executes pip using the currently selected Python interpreter.

This helps prevent accidentally installing packages into the wrong Python environment.

## 4. VS Code Integration

1. Open your project folder in VS Code.
2. Press `Ctrl + Shift + P`.
3. Search for `Python: Select Interpreter`.
4. Select the Python executable inside your `.venv` or `env1` folder.
5. Open a new terminal.
6. Verify the interpreter.

Windows:

```powershell
where.exe python
```

Linux:

```bash
which python
```

VS Code can automatically activate the selected environment in a new integrated terminal.

---

# PART 11 – Teaching Questions

Ask students these questions after completing the practical.

**Q1. If we install pandas in env1, will it automatically be available in env2?**

Answer: No. Each environment has its own package installation directory.

**Q2. Does deactivate delete the virtual environment?**

Answer: No. It only exits the currently active environment.

**Q3. Can we activate env1 again after deactivating it?**

Answer: Yes. The environment remains on disk until it is deleted.

**Q4. If we delete env1, will env2 also be deleted?**

Answer: No. They are independent directories.

**Q5. Why do we need requirements.txt?**

Answer: It records dependencies and their versions so another developer or machine can recreate the environment.

**Q6. Can two environments use different versions of the same package?**

Answer: Yes. For example, env1 can use pandas 2.x and env2 can use another compatible pandas version.

**Q7. Does a virtual environment install a new operating system?**

Answer: No. It provides an isolated Python package environment.

**Q8. What happens if we run a project without activating its required environment?**

Answer: It may use another Python interpreter and fail with ModuleNotFoundError if the required dependencies are not installed there.

---

# PART 12 – Final Classroom Demonstration

Perform this sequence in front of students.

### Demonstration 1

```bash
python -m venv env1
```

Activate env1 and install:

```bash
python -m pip install requests pandas
```

Run:

```bash
python -c "import pandas; print('Environment 1 Working')"
```

### Demonstration 2

Deactivate and create env2:

```bash
deactivate
python -m venv env2
```

Activate env2 and install:

```bash
python -m pip install flask numpy
```

Run:

```bash
python -c "import flask; print('Environment 2 Working')"
```

### Demonstration 3 – Prove Isolation

Inside env2:

```bash
python -c "import requests"
```

It should fail.

Switch to env1:

```bash
deactivate
```

```bash
# Windows
.\env1\Scripts\Activate.ps1

# Linux
source env1/bin/activate
```

Now:

```bash
python -c "import requests; print('Requests Available')"
```

It should work.

### Demonstration 4 – Cleanup

```bash
deactivate
```

Delete both environments.

Windows:

```powershell
Remove-Item -Recurse -Force env1, env2
```

Linux:

```bash
rm -rf env1 env2
```

---

# Final Conclusion

A Python Virtual Environment is important because it provides dependency isolation between projects.

Think of it like having two separate classrooms:

- Classroom 1 has its own books and equipment.
- Classroom 2 has different books and equipment.
- Removing Classroom 1 does not affect Classroom 2.

Similarly, Python environments allow different projects to manage their own packages independently.

**Remember these four commands:**

```bash
# Create
python -m venv env1

# Activate
source env1/bin/activate

# Exit
deactivate

# Delete
rm -rf env1
```

Windows PowerShell uses its own activation and deletion commands, as covered in the practical above.

**Golden Rule:** Create one virtual environment for each Python project, keep a requirements.txt file, and never commit the virtual environment directory to GitHub.