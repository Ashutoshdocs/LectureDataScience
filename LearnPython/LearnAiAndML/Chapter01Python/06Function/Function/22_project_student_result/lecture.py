"""Lecture 22: Project: student result system built as a pipeline of small functions."""
import functools
import time

SUBJECTS = ("Maths", "Science", "English", "History", "Computer")
PASS_MARK = 35
GRADE_BANDS = [(90, "A+"), (80, "A"), (70, "B"), (60, "C"), (50, "D"), (35, "E")]

RAW_DATA = """\
101, Asha Rao,    95, 88, 92, 79, 99
102, Ravi Kumar,  45, 33, 60, 52, 70
103, Dev Patel,   78, 85, 69, 88, 91
104, Meena Iyer,  30, 28, 55, 40, 62
105, Omar Shaikh, 66, 72, abc, 58, 80
106, Lina Das,    88, 91, 84, 95, 87
107, Kiran Joshi, 70, 65, 110, 60, 75
108, Sara Khan,   34, 50, 48, 61, 57"""


class InvalidMarks(ValueError):
    """Raised when a row's marks are missing, non-numeric or out of range."""


# ---------- decorator ----------
def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"  [{func.__name__} took {(time.perf_counter() - start) * 1000:.3f} ms]")
        return result
    return wrapper


# ---------- 1. parse & validate ----------
def validate_marks(marks):
    if len(marks) != len(SUBJECTS):
        raise InvalidMarks(f"expected {len(SUBJECTS)} marks, got {len(marks)}")
    clean = []
    for subject, m in zip(SUBJECTS, marks):
        try:
            value = int(m)
        except ValueError:
            raise InvalidMarks(f"{subject} mark {m!r} is not a number") from None
        if not 0 <= value <= 100:
            raise InvalidMarks(f"{subject} mark {value} is outside 0-100")
        clean.append(value)
    return clean


def parse_line(line):
    roll, name, *marks = [part.strip() for part in line.split(",")]
    return {"roll": int(roll), "name": name, "marks": validate_marks(marks)}


def parse_all(text, errors):
    """Generator: yields good records, appends bad rows to `errors`."""
    for line_no, line in enumerate(text.splitlines(), start=1):
        try:
            yield parse_line(line)
        except InvalidMarks as e:
            errors.append(f"line {line_no}: {e}")


# ---------- 2. pure calculations ----------
def total(marks):
    return sum(marks)


def percentage(marks):
    return round(total(marks) / (len(marks) * 100) * 100, 2)


def grade(pct):
    for cutoff, letter in GRADE_BANDS:
        if pct >= cutoff:
            return letter
    return "F"


def failed_subjects(marks, pass_mark=PASS_MARK):
    return [s for s, m in zip(SUBJECTS, marks) if m < pass_mark]


def result_status(marks):
    failed = failed_subjects(marks)
    return "PASS" if not failed else f"FAIL ({', '.join(failed)})"


# ---------- 3. pipeline steps (record -> record) ----------
def add_scores(student):
    m = student["marks"]
    return {**student, "total": total(m), "percent": percentage(m)}


def add_grade(student):
    return {**student, "grade": grade(student["percent"]) if not failed_subjects(student["marks"]) else "F"}


def add_result(student):
    return {**student, "result": result_status(student["marks"])}


def make_grace_marks(max_grace):
    """Closure: returns a step that lifts marks just below PASS_MARK."""
    def apply_grace(student):
        marks = list(student["marks"])
        used = 0
        for i, m in enumerate(marks):
            need = PASS_MARK - m
            if 0 < need <= max_grace - used:
                marks[i] += need
                used += need
        return {**student, "marks": marks, "grace": used}
    return apply_grace


def compose(*steps):
    """Combine several record->record functions into one."""
    def pipeline(record):
        for step in steps:
            record = step(record)
        return record
    return pipeline


# ---------- 4. ranking & stats ----------
def rank_students(students, key=lambda s: s["percent"]):
    ranked = sorted(students, key=key, reverse=True)
    return [{**s, "rank": i} for i, s in enumerate(ranked, start=1)]


def subject_stats(students):
    columns = zip(*(s["marks"] for s in students))
    return {subj: {"avg": round(sum(col) / len(col), 1), "max": max(col), "min": min(col)}
            for subj, col in zip(SUBJECTS, columns)}


# ---------- 5. output ----------
def report_card(student, *, width=40):
    line = "-" * width
    rows = [line, f"Roll {student['roll']}  {student['name']}".center(width), line]
    rows += [f"{subj:<12}{m:>5}{'  *' if m < PASS_MARK else ''}" for subj, m in zip(SUBJECTS, student["marks"])]
    rows += [line, f"{'Total':<12}{student['total']:>5} / {len(SUBJECTS) * 100}",
             f"{'Percent':<12}{student['percent']:>5}%",
             f"{'Grade':<12}{student['grade']:>5}",
             f"Result: {student['result']}"]
    if student.get("grace"):
        rows.append(f"(includes {student['grace']} grace mark(s))")
    return "\n".join("  " + r for r in rows + [line])


# ---------- tests ----------
def run_tests():
    assert total([10, 20, 30]) == 60
    assert percentage([50] * 5) == 50
    assert [grade(p) for p in (95, 80, 72.5, 34.9)] == ["A+", "A", "B", "F"]
    assert failed_subjects([34, 35, 90, 0, 100]) == ["Maths", "History"]
    assert make_grace_marks(3)({"marks": [33, 90, 90, 90, 90]})["marks"][0] == 35
    try:
        validate_marks(["1", "2"])
    except InvalidMarks:
        pass
    else:
        raise AssertionError("validate_marks should reject short rows")
    print("  all unit tests passed")


@timed
def process(text, *steps):
    errors = []
    pipeline = compose(*steps)
    students = [pipeline(record) for record in parse_all(text, errors)]
    return students, errors


def main():
    print("=== Unit tests first ===")
    run_tests()

    print("\n=== Run the pipeline ===")
    students, errors = process(RAW_DATA, add_scores, add_grade, add_result)
    print(f"  {len(students)} valid students, {len(errors)} rejected rows:")
    for err in errors:
        print("   ", err)

    print("\n=== Class result ===")
    print(f"  {'Rank':<5}{'Roll':<6}{'Name':<13}{'Total':>6}{'%':>8}  Grade  Result")
    for s in rank_students(students):
        print(f"  {s['rank']:<5}{s['roll']:<6}{s['name']:<13}{s['total']:>6}{s['percent']:>8}  {s['grade']:<5}  {s['result']}")

    print("\n=== Subject statistics ===")
    for subj, st in subject_stats(students).items():
        print(f"  {subj:<10} avg {st['avg']:>5}  max {st['max']:>3}  min {st['min']:>3}")
    passed = [s for s in students if s["result"] == "PASS"]
    print(f"  pass rate: {len(passed)}/{len(students)} = {len(passed) / len(students):.0%}")

    print("\n=== Top report card ===")
    print(report_card(rank_students(students)[0]))

    print("\n=== Same pipeline + one extra step: up to 3 grace marks ===")
    graced, _ = process(RAW_DATA, make_grace_marks(3), add_scores, add_grade, add_result)
    before = {s["roll"]: s["result"] for s in students}
    for s in graced:
        if s["grace"]:
            print(f"  {s['name']:<12} before: {before[s['roll']]:<28} after: {s['result']}")
    print()
    print(report_card(next(s for s in graced if s["roll"] == 108), width=36))


if __name__ == "__main__":
    main()
