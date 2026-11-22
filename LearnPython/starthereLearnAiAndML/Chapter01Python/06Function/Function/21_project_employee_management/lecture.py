"""Lecture 21: Project: employee management (CRUD) with functions only."""
import functools

AUDIT_LOG = []
CURRENT_USER = {"name": "hr_admin", "is_admin": True}
ALLOWED_FIELDS = {"name", "dept", "salary", "skills", "city", "phone"}
DEPARTMENTS = {"IT", "HR", "Sales", "Finance"}


# ---------- generator ----------
def id_generator(prefix="EMP"):
    n = 0
    while True:
        n += 1
        yield f"{prefix}-{n:04d}"


NEXT_ID = id_generator()


# ---------- decorators ----------
def audit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        def show(v):                                       # functions print as their name
            return v.__name__ if callable(v) else repr(v)
        parts = [show(a) for a in args[1:]]                # skip the db argument
        parts += [f"{k}={show(v)}" for k, v in kwargs.items()]
        AUDIT_LOG.append(f"{func.__name__}({', '.join(parts)})")
        return result
    return wrapper


def require_admin(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not CURRENT_USER["is_admin"]:
            raise PermissionError(f"{CURRENT_USER['name']} may not call {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


# ---------- validation ----------
def validate_employee(name, dept, salary):
    if not isinstance(name, str) or len(name.strip()) < 2:
        raise ValueError("name must be at least 2 characters")
    if dept not in DEPARTMENTS:
        raise ValueError(f"unknown department {dept!r}; choose from {sorted(DEPARTMENTS)}")
    if not isinstance(salary, (int, float)) or salary <= 0:
        raise ValueError("salary must be a positive number")


# ---------- CRUD ----------
@audit
def add_employee(db, name, dept, salary, *skills, **extra):
    validate_employee(name, dept, salary)
    unknown = set(extra) - ALLOWED_FIELDS
    if unknown:
        raise ValueError(f"unknown field(s): {sorted(unknown)}")
    emp = {"id": next(NEXT_ID), "name": name.strip().title(), "dept": dept,
           "salary": salary, "skills": list(skills), **extra}
    db.append(emp)
    return emp


def find_employee(db, emp_id):
    return next((e for e in db if e["id"] == emp_id), None)


@audit
def update_employee(db, emp_id, **changes):
    emp = find_employee(db, emp_id)
    if emp is None:
        raise KeyError(f"no employee {emp_id}")
    unknown = set(changes) - ALLOWED_FIELDS
    if unknown:
        raise ValueError(f"unknown field(s): {sorted(unknown)}")
    merged = {**emp, **changes}
    validate_employee(merged["name"], merged["dept"], merged["salary"])
    emp.update(changes)
    return emp


@audit
@require_admin
def delete_employee(db, emp_id):
    emp = find_employee(db, emp_id)
    if emp is None:
        return False
    db.remove(emp)
    return True


# ---------- queries ----------
def search(db, *, dept=None, min_salary=0, skill=None):
    return [e for e in db
            if (dept is None or e["dept"] == dept)
            and e["salary"] >= min_salary
            and (skill is None or skill in e["skills"])]


@audit
def give_raise(db, percent, *, where=lambda e: True):
    changed = []
    for e in db:
        if where(e):
            e["salary"] = round(e["salary"] * (1 + percent / 100))
            changed.append(e["name"])
    return changed


def department_summary(db):
    summary = {}
    for e in db:
        summary.setdefault(e["dept"], []).append(e)
    return {dept: {"count": len(staff),
                   "payroll": sum(e["salary"] for e in staff),
                   "top": max(staff, key=lambda e: e["salary"])["name"]}
            for dept, staff in sorted(summary.items())}


def payroll_report(db, sort_by="salary", descending=True):
    rows = sorted(db, key=lambda e: e[sort_by], reverse=descending)
    print(f"  {'ID':<9}{'Name':<14}{'Dept':<8}{'Salary':>9}  Skills")
    for e in rows:
        print(f"  {e['id']:<9}{e['name']:<14}{e['dept']:<8}{e['salary']:>9,}  {', '.join(e['skills']) or '-'}")
    print(f"  {'':<31}{sum(e['salary'] for e in db):>9,}  (total)")


def main():
    db = []
    print("=== Create ===")
    add_employee(db, "asha rao", "IT", 60000, "python", "sql", city="Pune")
    add_employee(db, "Ravi Kumar", "HR", 45000, "excel")
    add_employee(db, "dev patel", "IT", 70000, "python", "aws", "docker")
    add_employee(db, "Meena Iyer", "Sales", 52000, phone="98765-43210")
    for bad in [("A", "IT", 1000), ("Zara", "Legal", 1000), ("Zara", "IT", -5)]:
        try:
            add_employee(db, *bad)
        except ValueError as e:
            print(f"  add_employee{bad} -> {e}")
    try:
        add_employee(db, "Omar", "IT", 40000, salry=1)
    except ValueError as e:
        print("  typo in **extra ->", e)
    payroll_report(db)

    print("\n=== Read / search ===")
    print("  find EMP-0002:", find_employee(db, "EMP-0002")["name"], "| find EMP-9999:", find_employee(db, "EMP-9999"))
    print("  IT staff        :", [e["name"] for e in search(db, dept="IT")])
    print("  python & >= 65k :", [e["name"] for e in search(db, skill="python", min_salary=65000)])
    try:
        search(db, "IT")
    except TypeError as e:
        print("  search(db, 'IT') ->", e, "(filters are keyword-only)")

    print("\n=== Update ===")
    update_employee(db, "EMP-0002", dept="Finance", city="Delhi")
    print("  Ravi now:", find_employee(db, "EMP-0002"))
    for bad in [{"salary": -1}, {"title": "boss"}]:
        try:
            update_employee(db, "EMP-0002", **bad)
        except ValueError as e:
            print(f"  update {bad} -> {e}")
    print("  10% raise for IT  :", give_raise(db, 10, where=lambda e: e["dept"] == "IT"))
    print("  5% raise < 50,000 :", give_raise(db, 5, where=lambda e: e["salary"] < 50000))

    print("\n=== Delete (admin only) ===")
    CURRENT_USER.update(name="intern", is_admin=False)
    try:
        delete_employee(db, "EMP-0004")
    except PermissionError as e:
        print("  ", e)
    CURRENT_USER.update(name="hr_admin", is_admin=True)
    print("  delete EMP-0004:", delete_employee(db, "EMP-0004"), "| again:", delete_employee(db, "EMP-0004"))

    print("\n=== Reports ===")
    payroll_report(db, sort_by="name", descending=False)
    for dept, info in department_summary(db).items():
        print(f"  {dept:<8} {info}")

    print("\n=== Audit log (from the @audit decorator) ===")
    for entry in AUDIT_LOG:
        print("  ", entry)


if __name__ == "__main__":
    main()
