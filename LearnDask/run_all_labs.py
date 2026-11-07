"""
Run all 20 Dask practical labs in one go.

Usage (from your system terminal, inside this folder):
    python run_all_labs.py

Each lab prints its title, the command, and the result, so learners can
compare their own Python Shell output with this reference run.
"""
import dask
import dask.dataframe as dd
import pandas as pd


def lab(title, command):
    print("=" * 70)
    print(title)
    print("-" * 70)
    print(">>>", command)
    result = eval(command)
    if result is not None:
        print(result)
    print()


lab("LAB 1 - CHECK DASK VERSION",
    'dask.__version__')

lab("LAB 2 - CREATE A DASK DATAFRAME",
    'dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya"],"Age":[25,30,28]}), npartitions=2).compute()')

lab("LAB 3 - CHECK NUMBER OF PARTITIONS",
    'dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya"]}), npartitions=2).npartitions')

lab("LAB 4 - DISPLAY FIRST TWO RECORDS",
    'dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya"],"Age":[25,30,28]}), npartitions=2).head(2)')

lab("LAB 5 - DISPLAY LAST TWO RECORDS",
    'dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya"],"Age":[25,30,28]}), npartitions=1).tail(2)')

lab("LAB 5 (gotcha) - tail() ONLY READS THE LAST PARTITION",
    'dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya"],"Age":[25,30,28]}), npartitions=2).tail(2)')

lab("LAB 6 - DISPLAY ONLY THE NAME COLUMN",
    'dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya"],"Age":[25,30,28]}), npartitions=2)["Name"].compute()')

lab("LAB 7 - FILTER AGE GREATER THAN 25",
    'dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya"],"Age":[25,30,28]}), npartitions=2).query("Age > 25").compute()')

lab("LAB 8 - FILTER AGE LESS THAN 30",
    'dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya"],"Age":[25,30,28]}), npartitions=2).query("Age < 30").compute()')

lab("LAB 9 - CALCULATE TOTAL SALARY",
    'dd.from_pandas(pd.DataFrame({"Salary":[30000,40000,50000]}), npartitions=2)["Salary"].sum().compute()')

lab("LAB 10 - CALCULATE AVERAGE SALARY",
    'dd.from_pandas(pd.DataFrame({"Salary":[30000,40000,50000]}), npartitions=2)["Salary"].mean().compute()')

lab("LAB 11 - FIND MAXIMUM SALARY",
    'dd.from_pandas(pd.DataFrame({"Salary":[30000,40000,50000]}), npartitions=2)["Salary"].max().compute()')

lab("LAB 12 - FIND MINIMUM SALARY",
    'dd.from_pandas(pd.DataFrame({"Salary":[30000,40000,50000]}), npartitions=2)["Salary"].min().compute()')

lab("LAB 13 - COUNT EMPLOYEE NAMES",
    'dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya","Neha"]}), npartitions=2)["Name"].count().compute()')

lab("LAB 14 - SORT EMPLOYEES BY SALARY",
    'dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya"],"Salary":[30000,50000,40000]}), npartitions=2).sort_values("Salary").compute()')

lab("LAB 15 - GROUP EMPLOYEES BY DEPARTMENT",
    'dd.from_pandas(pd.DataFrame({"Department":["IT","HR","IT","HR"],"Salary":[30000,20000,40000,25000]}), npartitions=2).groupby("Department")["Salary"].sum().compute()')

lab("LAB 16 - CREATE A CSV FILE",
    'pd.DataFrame({"Name":["Rahul","Amit","Priya"],"Age":[25,30,28]}).to_csv("employees.csv", index=False)')

lab("LAB 17 - READ CSV USING DASK",
    'dd.read_csv("employees.csv").compute()')

lab("LAB 18 - CHECK PARTITIONS IN THE CSV",
    'dd.read_csv("employees.csv").npartitions')

lab("LAB 19 - SAVE DASK DATAFRAME INTO CSV",
    'dd.read_csv("employees.csv").to_csv("dask_output/employee-*.csv", index=False)')

EMP = 'dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya","Neha"],"Salary":[30000,40000,35000,45000]}), npartitions=2)'
lab("LAB 20a - TOTAL NUMBER OF EMPLOYEES", EMP + '["Name"].count().compute()')
lab("LAB 20b - TOTAL SALARY",              EMP + '["Salary"].sum().compute()')
lab("LAB 20c - AVERAGE SALARY",            EMP + '["Salary"].mean().compute()')
lab("LAB 20d - HIGHEST SALARY",            EMP + '["Salary"].max().compute()')
lab("LAB 20e - LOWEST SALARY",             EMP + '["Salary"].min().compute()')

lab("BONUS - LAZY EXECUTION (no compute)",
    'dd.from_pandas(pd.DataFrame({"Salary":[30000,40000,50000]}), npartitions=2)["Salary"].sum()')
lab("BONUS - LAZY EXECUTION (with compute)",
    'dd.from_pandas(pd.DataFrame({"Salary":[30000,40000,50000]}), npartitions=2)["Salary"].sum().compute()')

print("All labs completed successfully.")
