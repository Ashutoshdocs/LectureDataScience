"""Lecture 20: Revision: a 20-question self-test (answers computed from real figures) and a chart-type cheat-sheet image."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import matplotlib  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import seaborn as sns  # noqa: E402
from matplotlib.container import BarContainer  # noqa: E402
from common import CATEGORIES, apply_style, get_market_share, get_monthly_sales, get_students, save_and_show  # noqa: E402

apply_style()
sales, students, share = get_monthly_sales(), get_students(), get_market_share()
QUESTIONS = []


def question(text):
    def register(func):
        QUESTIONS.append((text, func))
        return func
    return register


@question("fig, ax = plt.subplots(2, 3): what is axes.shape?")
def q01():
    fig, axes = plt.subplots(2, 3)
    return axes.shape


@question("What type is `ax` from fig, ax = plt.subplots()? (careful: Axes is not 'axis')")
def q02():
    _, ax = plt.subplots()
    return type(ax).__name__


@question("ax.plot(...) returns ... ?")
def q03():
    _, ax = plt.subplots()
    out = ax.plot([1, 2], [3, 4])
    return f"a {type(out).__name__} of {type(out[0]).__name__} objects"


@question("plt.title() after creating two subplots changes which Axes?")
def q04():
    fig, (a, b) = plt.subplots(1, 2)
    plt.title("X")
    return "the LAST (current) one" if b.get_title() == "X" and a.get_title() == "" else "?"


@question("figsize=(6, 4) saved with dpi=150: image width in pixels?")
def q05():
    return 6 * 150


@question("Grouped bars: 3 series, width=0.27. Offsets of the bars around each group centre?")
def q06():
    w = 0.27
    return [-w, 0, w]


@question("Stacked bars: which argument makes a series start where the previous ended?")
def q07():
    _, ax = plt.subplots()
    ax.bar([0], [5])
    bars = ax.bar([0], [3], bottom=[5])
    return f"bottom= (second bar starts at y={bars[0].get_y():.0f})"


@question("ax.barh draws categories bottom-to-top. Which sort order puts the LARGEST at the top?")
def q08():
    return "ascending (sort_values())"


@question("Which pie argument turns a pie into a donut?")
def q09():
    _, ax = plt.subplots()
    wedges, _ = ax.pie([1, 2, 3], wedgeprops={"width": 0.4})
    return f"wedgeprops={{'width': 0.4}} (wedge width = {wedges[0].width})"


@question("ax.hist(scores, bins=range(0, 101, 10)) draws how many bars?")
def q10():
    _, ax = plt.subplots()
    counts, edges, patches = ax.hist(students["score"], bins=range(0, 101, 10))
    return len(patches)


@question("With hist(density=True), what do the bar areas add up to?")
def q11():
    counts, edges = np.histogram(students["score"], bins=10, density=True)
    return round(float((counts * np.diff(edges)).sum()), 3)


@question("Correlation r between study_hours and score in the student data?")
def q12():
    return round(float(students["study_hours"].corr(students["score"])), 2)


@question("A perfect U-shaped relationship has r close to ... ?")
def q13():
    x = np.linspace(-3, 3, 101)
    return abs(round(float(np.corrcoef(x, x ** 2)[0, 1]), 3))


@question("Which is the Matplotlib tool for 50,000 overlapping scatter points?")
def q14():
    _, ax = plt.subplots()
    hb = ax.hexbin(np.random.default_rng(0).normal(size=1000), np.random.default_rng(1).normal(size=1000))
    return f"ax.hexbin (returns a {type(hb).__name__})"


@question("sns.scatterplot(..., ax=ax) returns ... ?  sns.lmplot(...) returns ... ?")
def q15():
    _, ax = plt.subplots()
    a = sns.scatterplot(data=students, x="study_hours", y="score", ax=ax)
    g = sns.lmplot(data=students, x="study_hours", y="score", height=2)
    return f"{type(a).__name__} / {type(g).__name__}"


@question("Wide sales table (12 x 4) melted to long format: shape?")
def q16():
    return sales.melt(id_vars="Month", var_name="Category", value_name="Sales").shape


@question("barplot default error bar shows ... ?")
def q17():
    import inspect
    return f"errorbar={inspect.signature(sns.barplot).parameters['errorbar'].default!r} (95% confidence interval of the mean)"


@question("Which palette type for 'above vs below target' values?")
def q18():
    return "diverging (e.g. 'vlag', 'RdBu', center=0)"


@question("A bar chart's y-axis should start at ... ?")
def q19():
    _, ax = plt.subplots()
    ax.bar(["a", "b"], [96, 99])
    return f"0 (Matplotlib's default for bars: ylim starts at {ax.get_ylim()[0]:.0f})"


@question("Hide the top and right spines with ... ?")
def q20():
    _, ax = plt.subplots()
    ax.spines[["top", "right"]].set_visible(False)
    return "ax.spines[['top', 'right']].set_visible(False)" if not ax.spines["top"].get_visible() else "?"


def cheat_sheet():
    """One image with every chart type from the course."""
    fig, axes = plt.subplots(3, 4, figsize=(20, 13))
    x = np.arange(12)
    rng = np.random.default_rng(0)
    axes[0, 0].plot(sales["Month"], sales["Electronics"], marker="o")
    axes[0, 0].set_title("line: ax.plot")
    axes[0, 1].bar(sales["Month"][:6], sales["Clothing"][:6], color="tab:orange")
    axes[0, 1].set_title("bar: ax.bar")
    tot = sales[CATEGORIES].sum().sort_values()
    axes[0, 2].barh(tot.index, tot.values, color="tab:green")
    axes[0, 2].set_title("horizontal: ax.barh")
    bottom = np.zeros(6)
    for cat in CATEGORIES:
        axes[0, 3].bar(sales["Month"][:6], sales[cat][:6], bottom=bottom)
        bottom += sales[cat][:6].to_numpy()
    axes[0, 3].set_title("stacked: bottom=")
    axes[1, 0].pie(share.values(), labels=share.keys(), wedgeprops={"width": 0.4}, textprops={"fontsize": 8})
    axes[1, 0].set_title("donut: ax.pie")
    axes[1, 1].stackplot(x, [sales[c] for c in CATEGORIES], alpha=0.85)
    axes[1, 1].set_title("stack: ax.stackplot")
    axes[1, 2].hist(students["score"], bins=15, color="slateblue", edgecolor="white")
    axes[1, 2].set_title("histogram: ax.hist")
    axes[1, 3].scatter(students["study_hours"], students["score"], c=students["sleep_hours"], s=12, cmap="viridis")
    axes[1, 3].set_title("scatter: ax.scatter(c=)")
    sns.boxplot(data=students, x="grade_level", y="score", order=["Freshman", "Sophomore", "Junior", "Senior"], ax=axes[2, 0])
    axes[2, 0].set_title("sns.boxplot")
    axes[2, 0].tick_params(axis="x", labelsize=8)
    sns.kdeplot(data=students, x="score", hue="gender", fill=True, ax=axes[2, 1])
    axes[2, 1].set_title("sns.kdeplot(hue=)")
    sns.heatmap(students[["study_hours", "sleep_hours", "score"]].corr(), annot=True, cmap="vlag", vmin=-1, vmax=1,
                ax=axes[2, 2], cbar=False)
    axes[2, 2].set_title("sns.heatmap")
    axes[2, 3].hexbin(rng.normal(size=5000), rng.normal(size=5000), gridsize=25, cmap="viridis")
    axes[2, 3].set_title("many points: ax.hexbin")
    for ax in axes[0, :2]:
        ax.tick_params(axis="x", labelsize=8, rotation=45)
    fig.suptitle("Cheat sheet: every chart type in this course", fontsize=20, fontweight="bold")
    save_and_show(fig, "20_cheat_sheet.png")


def main():
    print(f"Self-test: {len(QUESTIONS)} questions (answers computed from real figures)\n")
    for number, (text, func) in enumerate(QUESTIONS, start=1):
        answer = func()
        plt.close("all")
        print(f"Q{number:02d}. {text}")
        print(f"     -> {answer!r}\n")
    assert len(QUESTIONS) == 20
    cheat_sheet()


if __name__ == "__main__":
    main()
