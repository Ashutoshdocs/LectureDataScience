# Lecture 21: Project: employee management

Run: `python lecture.py`

A small HR system that stores employees as a **list of dicts** and manages them with **functions only** (no classes), the classic CRUD pattern: **C**reate, **R**ead, **U**pdate, **D**elete.

## Data

```python
employee = {"id": "EMP-0001", "name": "Asha Rao", "dept": "IT", "salary": 60000, "skills": ["python", "sql"]}
```

## Functions and what they teach

| Function | Lectures | Notes |
|----------|----------|-------|
| `id_generator(prefix)` | 17 | **generator** producing `EMP-0001`, `EMP-0002`, … |
| `validate_employee(name, dept, salary)` | 18 | raises `ValueError` with clear messages |
| `add_employee(db, name, dept, salary, *skills, **extra)` | 06, 07 | `*skills` for any number of skills; `**extra` for optional fields (city, phone…) |
| `find_employee(db, emp_id)` | 04 | returns the dict or `None` |
| `update_employee(db, emp_id, **changes)` | 07, 18 | change only the given fields; rejects unknown fields |
| `delete_employee(db, emp_id)` | 04 | returns `True`/`False` |
| `search(db, *, dept=None, min_salary=0, skill=None)` | 08 | keyword-only filters |
| `give_raise(db, percent, *, where=lambda e: True)` | 10, 11 | a **function as a parameter** decides who gets the raise |
| `department_summary(db)` | 12 | grouping with dicts; `sum`, `max(key=)` |
| `payroll_report(db, sort_by="salary")` | 11, 12 | `sorted(key=lambda …)` |
| `@audit` | 14, 15 | decorator that logs every change with the function name and arguments |
| `@require_admin` | 15 | decorator with access control |

## Why a list of dicts + functions?

It's the simplest design that works, and it's how JSON / API data arrives. Once the functions all take `db` as their first argument and repeat the same patterns, you've rediscovered **why classes exist**. That's the natural next step (see the Classes & Objects course).

## Extension exercises

1. Save `db` to `employees.json` and load it at start-up (`json.dump` / `json.load`).
2. Add `promote(db, emp_id, new_dept, raise_percent)` built from the existing functions.
3. Add a decorator `@undoable` that stores the previous state so the last change can be undone.
4. Add `top_earners(db, n=3)`.

**Next →** [Lecture 22: Project: student result](../22_project_student_result/)
