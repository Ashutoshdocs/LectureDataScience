# Python Environment Setup for Data Science and Machine Learning

A beginner-friendly guide to creating an isolated Python environment and
installing commonly used data science, analytics, and machine learning
libraries.

This guide covers **Windows**, **Linux**, and **macOS**.

------------------------------------------------------------------------

## 1. What you will install

  -----------------------------------------------------------------------
  Library / Tool          Purpose                 Install package
  ----------------------- ----------------------- -----------------------
  NumPy                   Numerical computing,    `numpy`
                          arrays, mathematical    
                          operations              

  pandas                  Data analysis and       `pandas`
                          tabular data            
                          manipulation            

  scikit-learn            Machine learning        `scikit-learn`
                          algorithms and model    
                          evaluation              

  Polars                  Fast DataFrame and      `polars`
                          data-processing library 

  Dask                    Parallel and            `dask`
                          larger-than-memory      
                          computing               

  Matplotlib              Data visualization and  `matplotlib`
                          plotting                

  Seaborn                 Statistical data        `seaborn`
                          visualization           

  JupyterLab              Interactive notebooks   `jupyterlab`
                          for learning and        
                          experiments             

  SciPy                   Scientific and          `scipy`
                          statistical computing   

  PyArrow                 Columnar data formats   `pyarrow`
                          and interoperability    
  -----------------------------------------------------------------------

> **Important:** The package is installed as `scikit-learn`, but
> imported in Python using `sklearn`.

------------------------------------------------------------------------

## 2. Install Python

Download Python from the official website:

<https://www.python.org/downloads/>

Choose a currently supported Python 3 release. During Windows
installation, select **Add Python to PATH**.

Verify the installation:

### Windows

``` powershell
py --version
py -m pip --version
```

If the `py` launcher is unavailable, try:

``` powershell
python --version
python -m pip --version
```

### Linux / macOS

``` bash
python3 --version
python3 -m pip --version
```

If Python or pip is missing on Ubuntu/Debian:

``` bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

------------------------------------------------------------------------

## 3. Create a project folder

Create a separate folder for your Python practice.

### Windows PowerShell

``` powershell
mkdir Python-DataScience
cd Python-DataScience
```

### Linux / macOS

``` bash
mkdir -p Python-DataScience
cd Python-DataScience
```

------------------------------------------------------------------------

## 4. Create a virtual environment

A virtual environment keeps project dependencies separate from other
Python projects.

### Windows PowerShell

``` powershell
py -m venv .venv
```

If you use `python` instead of `py`:

``` powershell
python -m venv .venv
```

### Linux / macOS

``` bash
python3 -m venv .venv
```

The `.venv` directory contains the isolated Python environment for this
project.

------------------------------------------------------------------------

## 5. Activate the virtual environment

Activate the environment before installing packages or running project
code.

### Windows PowerShell

``` powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation scripts, you can allow scripts for the
current PowerShell process only:

``` powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### Windows Command Prompt (CMD)

``` cmd
.venv\Scripts\activate.bat
```

### Linux / macOS

``` bash
source .venv/bin/activate
```

When activated, the terminal normally displays `(.venv)` at the
beginning of the prompt.

To confirm which Python is being used:

**Windows:**

``` powershell
where.exe python
```

**Linux / macOS:**

``` bash
which python
```

The path should point inside your project's `.venv` directory.

------------------------------------------------------------------------

## 6. Upgrade pip

With the virtual environment activated, upgrade pip:

``` bash
python -m pip install --upgrade pip
```

Using `python -m pip` helps ensure that packages are installed into the
Python interpreter belonging to the active environment.

------------------------------------------------------------------------

## 7. Install the libraries

Install all the main data science and machine learning libraries in one
command:

``` bash
python -m pip install numpy pandas scikit-learn polars "dask[complete]" matplotlib seaborn jupyterlab scipy pyarrow
```

### Install libraries individually

If you prefer to teach or install each library separately:

``` bash
python -m pip install numpy
python -m pip install pandas
python -m pip install scikit-learn
python -m pip install polars
python -m pip install "dask[complete]"
python -m pip install matplotlib
python -m pip install seaborn
python -m pip install jupyterlab
python -m pip install scipy
python -m pip install pyarrow
```

**Why use `dask[complete]`?** It installs Dask with a broader set of
optional dependencies for common DataFrame, array,
distributed-computing, and dashboard workflows. If you only need the
basic Dask package, use:

``` bash
python -m pip install dask
```

------------------------------------------------------------------------

## 8. Create a `requirements.txt` file

A requirements file records the packages needed by the project. Create a
file named `requirements.txt` in the project folder:

``` text
numpy
pandas
scikit-learn
polars
dask[complete]
matplotlib
seaborn
jupyterlab
scipy
pyarrow
```

Install everything listed in the file:

``` bash
python -m pip install -r requirements.txt
```

To save the exact versions installed in your current environment:

``` bash
python -m pip freeze > requirements-lock.txt
```

To recreate an environment using that snapshot:

``` bash
python -m pip install -r requirements-lock.txt
```

For teaching projects, keep `requirements.txt` as the human-maintained
list of direct dependencies. Use a lock file when you need to reproduce
a particular installed set of versions.

------------------------------------------------------------------------

## 9. Verify the installation

Run this command while the virtual environment is activated:

``` bash
python -c "import numpy, pandas, sklearn, polars, dask, matplotlib, seaborn, scipy, pyarrow; print('All libraries imported successfully!'); print('NumPy:', numpy.__version__); print('pandas:', pandas.__version__); print('scikit-learn:', sklearn.__version__); print('Polars:', polars.__version__); print('Dask:', dask.__version__)"
```

You can also view installed packages:

``` bash
python -m pip list
```

Check dependency consistency:

``` bash
python -m pip check
```

------------------------------------------------------------------------

## 10. Create a first Python test program

Create a file named `test_environment.py`:

``` python
import numpy as np
import pandas as pd
import sklearn
import polars as pl
import dask.dataframe as dd

# NumPy: numerical array
numbers = np.array([10, 20, 30, 40])
print("NumPy array:", numbers)
print("Mean:", numbers.mean())

# pandas: tabular data
data = {
    "Name": ["Amit", "Priya", "Rahul"],
    "Marks": [85, 92, 78],
}
df = pd.DataFrame(data)
print("\npandas DataFrame:")
print(df)

# scikit-learn: import a machine learning utility
from sklearn.model_selection import train_test_split
print("\nscikit-learn version:", sklearn.__version__)

# Polars: DataFrame
polars_df = pl.DataFrame(data)
print("\nPolars DataFrame:")
print(polars_df)

# Dask: parallel/lazy DataFrame workflow
dask_df = dd.from_pandas(df, npartitions=2)
print("\nDask DataFrame result:")
print(dask_df.compute())

print("\nEnvironment setup successful!")
```

Run it:

``` bash
python test_environment.py
```

------------------------------------------------------------------------

## 11. Start JupyterLab

Start JupyterLab from the activated virtual environment:

``` bash
jupyter lab
```

Your browser should open the JupyterLab interface. Create a Python
notebook and try:

``` python
import numpy as np
import pandas as pd
import sklearn
import polars as pl
import dask.dataframe as dd

print("Python data science environment is ready!")
```

To stop JupyterLab, return to the terminal and press `Ctrl + C`.

------------------------------------------------------------------------

## 12. Recommended project structure

``` text
Python-DataScience/
│
├── .venv/
│
├── notebooks/
│   ├── 01_numpy.ipynb
│   ├── 02_pandas.ipynb
│   ├── 03_polars.ipynb
│   ├── 04_dask.ipynb
│   └── 05_machine_learning.ipynb
│
├── datasets/
│   └── students.csv
│
├── src/
│   └── test_environment.py
│
├── requirements.txt
├── requirements-lock.txt
└── README.md
```

Do not commit or share the `.venv` directory. It is machine-specific and
can be recreated from the requirements file.

A useful `.gitignore` file:

``` gitignore
.venv/
__pycache__/
*.py[cod]
.ipynb_checkpoints/
.env
```

------------------------------------------------------------------------

## 13. Deactivate or reactivate the environment

Deactivate the current environment:

``` bash
deactivate
```

Next time you work on the project, open a terminal in the project folder
and activate it again.

**Windows PowerShell:**

``` powershell
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

``` bash
source .venv/bin/activate
```

You do not need to recreate the environment every time.

------------------------------------------------------------------------

## 14. Common problems and solutions

### Problem 1: `python` is not recognized

Python may not be on your PATH.

-   On Windows, try `py --version`.
-   If Python is not installed, install it from
    <https://www.python.org/downloads/>.
-   Reopen the terminal after installation.

### Problem 2: `No module named 'numpy'`

The package may have been installed into a different Python environment.

Activate `.venv`, then run:

``` bash
python -m pip install numpy
```

Check the interpreter path:

``` bash
python -c "import sys; print(sys.executable)"
```

### Problem 3: PowerShell cannot run the activation script

Run this in the current PowerShell window:

``` powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate:

``` powershell
.\.venv\Scripts\Activate.ps1
```

Alternatively, use Command Prompt and run `.venv\Scripts\activate.bat`.

### Problem 4: `pip` installs into the wrong Python

Prefer:

``` bash
python -m pip install package_name
```

rather than using `pip` by itself. Confirm that the virtual environment
is active.

### Problem 5: Package installation fails

Try upgrading pip:

``` bash
python -m pip install --upgrade pip setuptools wheel
```

Then retry the installation. Also check that your Python version and
operating system are supported by the package versions being installed.

### Problem 6: `sklearn` installation or import confusion

Install:

``` bash
python -m pip install scikit-learn
```

Import:

``` python
import sklearn
```

Do not use `pip install sklearn` for a normal scikit-learn setup.

------------------------------------------------------------------------

## 15. Useful commands cheat sheet

  ------------------------------------------------------------------------------------
  Task                                Command
  ----------------------------------- ------------------------------------------------
  Check Python                        `python --version`

  Create environment                  `python -m venv .venv`

  Activate on Windows PowerShell      `.\.venv\Scripts\Activate.ps1`

  Activate on Linux/macOS             `source .venv/bin/activate`

  Upgrade pip                         `python -m pip install --upgrade pip`

  Install requirements                `python -m pip install -r requirements.txt`

  List packages                       `python -m pip list`

  Check dependencies                  `python -m pip check`

  Save installed versions             `python -m pip freeze > requirements-lock.txt`

  Launch JupyterLab                   `jupyter lab`

  Deactivate environment              `deactivate`
  ------------------------------------------------------------------------------------

------------------------------------------------------------------------

## 16. Recommended learning order

1.  **NumPy** --- arrays, indexing, slicing, broadcasting, and
    vectorized operations.
2.  **pandas** --- Series, DataFrames, CSV files, filtering, grouping,
    and missing values.
3.  **Polars** --- expressions, DataFrames, lazy execution, and
    efficient data transformations.
4.  **Dask** --- partitions, lazy computation, and parallel processing
    of larger datasets.
5.  **Matplotlib and Seaborn** --- charts and data visualization.
6.  **scikit-learn** --- preprocessing, train/test split, regression,
    classification, clustering, and model evaluation.

------------------------------------------------------------------------

## Official documentation

-   Python: <https://docs.python.org/3/>
-   `venv`: <https://docs.python.org/3/library/venv.html>
-   pip: <https://pip.pypa.io/en/stable/>
-   NumPy: <https://numpy.org/doc/>
-   pandas: <https://pandas.pydata.org/docs/>
-   scikit-learn: <https://scikit-learn.org/stable/>
-   Polars: <https://docs.pola.rs/>
-   Dask: <https://docs.dask.org/>
-   Matplotlib: <https://matplotlib.org/stable/>
-   Seaborn: <https://seaborn.pydata.org/>
-   JupyterLab: <https://jupyterlab.readthedocs.io/>

------------------------------------------------------------------------

**Setup complete!** You now have an isolated Python environment ready
for data analysis, data engineering experiments, visualization, and
machine learning practice.
