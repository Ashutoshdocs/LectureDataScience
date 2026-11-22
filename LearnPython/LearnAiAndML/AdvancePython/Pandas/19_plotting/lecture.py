"""Lecture 19: Plotting with df.plot(). Charts are saved to output/ as PNG files."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")                     # draw to files, no window needed
import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)

sales = pd.read_csv(DATA / "sales.csv", parse_dates=["date"])
sales["revenue"] = sales["units"] * sales["unit_price"]
students = pd.read_csv(DATA / "students.csv")
BLUE = "#2f62c9"


def save(ax, name):
    ax.figure.savefig(OUT / name, dpi=150, bbox_inches="tight")
    plt.close(ax.figure)
    print("saved output/" + name)


# 1. Line: revenue by month
monthly = sales.set_index("date")["revenue"].resample("ME").sum() / 1e5
monthly.index = monthly.index.strftime("%b")
save(monthly.plot(kind="line", marker="o", color=BLUE, figsize=(8, 4), grid=True,
                  title="Revenue by month, 2025", ylabel="Revenue (Rs lakh)", xlabel=""),
     "01_line_monthly.png")

# 2. Horizontal bar: revenue by region, sorted
by_region = sales.groupby("region")["revenue"].sum().sort_values() / 1e5
save(by_region.plot(kind="barh", color=BLUE, figsize=(6, 3),
                    title="Revenue by region", xlabel="Revenue (Rs lakh)", ylabel=""),
     "02_barh_region.png")

# 3. Bar: units per product
units = sales.groupby("product")["units"].sum().sort_values(ascending=False)
save(units.plot.bar(color=BLUE, rot=30, figsize=(7, 3.5), legend=False,
                    title="Units sold by product", ylabel="Units", xlabel=""),
     "03_bar_units.png")

# 4. Stacked bar: region x category
stack = sales.pivot_table(index="region", columns="category", values="revenue", aggfunc="sum") / 1e5
save(stack.plot(kind="bar", stacked=True, rot=0, figsize=(6, 4), color=[BLUE, "#e8a33d"],
                title="Revenue by region and category", ylabel="Revenue (Rs lakh)", xlabel=""),
     "04_stacked_region_category.png")

# 5. Histogram: order revenue
save(sales["revenue"].plot.hist(bins=20, color=BLUE, figsize=(6, 3.5),
                                title="Distribution of order revenue", xlabel="Revenue (Rs)"),
     "05_hist_revenue.png")

# 6. Box: marks per subject
save(students[["maths", "science", "english", "cs"]].plot.box(figsize=(6, 4), title="Marks by subject",
                                                               ylabel="Mark"),
     "06_box_marks.png")

# 7. Scatter: maths vs science
save(students.plot.scatter(x="maths", y="science", color=BLUE, s=40, figsize=(5, 4),
                           title="Maths vs science", grid=True),
     "07_scatter_maths_science.png")

# 8. Line: weekly order count
weekly = sales.set_index("date")["order_id"].resample("W").count()
save(weekly.plot(color=BLUE, figsize=(8, 3), title="Orders per week", ylabel="Orders", xlabel=""),
     "08_line_weekly_orders.png")

# 9. Several charts in one figure
fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
by_region.plot.barh(ax=axes[0], color=BLUE, title="By region (Rs lakh)", ylabel="")
(sales.groupby("category")["revenue"].sum() / 1e5).plot.bar(ax=axes[1], color=BLUE, rot=0,
                                                             title="By category (Rs lakh)", xlabel="")
fig.tight_layout()
save(axes[0], "09_two_panels.png")

print(f"\n{len(list(OUT.glob('*.png')))} charts in {OUT}")
