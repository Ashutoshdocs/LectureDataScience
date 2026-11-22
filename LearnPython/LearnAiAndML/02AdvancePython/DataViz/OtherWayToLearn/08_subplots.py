import matplotlib.pyplot as plt
from common import (
    apply_style,
    get_market_share,
    get_monthly_sales,
    get_students,
    save_and_show,
)

apply_style()
sales = get_monthly_sales()
students = get_students()
share = get_market_share()

# --- 1. Regular 2x2 grid: axes is a 2D array -> axes[row, col] ---
# Creates a structured bounding canvas containing 2 rows and 2 columns of equal sizes
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Accesses top-left subplot at row 0, column 0
axes[0, 0].plot(sales["Month"], sales["Electronics"], marker="o")
axes[0, 0].set_title("Line: Electronics")

# Accesses top-right subplot at row 0, column 1
axes[0, 1].bar(sales["Month"], sales["Clothing"], color="orange")
axes[0, 1].set_title("Bar: Clothing")
axes[0, 1].tick_params(
    axis="x", rotation=45
)  # Rotates X-axis labels by 45 degrees to prevent overlapping text

# Accesses bottom-left subplot at row 1, column 0
axes[1, 0].hist(students["score"], bins=15, edgecolor="white")
axes[1, 0].set_title("Histogram: Scores")

# Accesses bottom-right subplot at row 1, column 1
axes[1, 1].scatter(students["study_hours"], students["score"], s=12)
axes[1, 1].set_title("Scatter: Study vs Score")

# Adds a single overarching global title pinned to the top of the entire canvas layout
fig.suptitle("2x2 Subplot Dashboard", fontsize=16, fontweight="bold")
save_and_show(fig, "08a_subplots_grid.png")

# --- 2. GridSpec: one wide chart on top, two below ---
fig = (
    plt.figure(figsize=(12, 8))
)  # Initializes a raw figure canvas object without preset subplots
gs = fig.add_gridspec(
    2, 2
)  # Carves a virtual 2x2 layout grid matrix framework behind the scenes

# 'gs[0, :]' grabs row 0 and uses slice colon notation (:) to span across all available columns
top = fig.add_subplot(gs[0, :])
left = fig.add_subplot(gs[1, 0])  # Grabs row 1, column 0
right = fig.add_subplot(gs[1, 1])  # Grabs row 1, column 1

# Plot data inside our newly customized asymmetric framework windows
top.stackplot(
    range(12),
    sales["Electronics"],
    sales["Clothing"],
    sales["Groceries"],
    labels=["Electronics", "Clothing", "Groceries"],
)
top.set_xticks(range(12), sales["Month"])
top.set_title("Stack Plot (spans full width)")
top.legend(loc="upper left")

left.pie(share.values(), labels=share.keys(), autopct="%1.0f%%")
left.set_title("Market Share")

right.barh(list(share.keys()), list(share.values()), color="teal")
right.set_title("Market Share (bars)")

fig.suptitle("Custom Layout with GridSpec", fontsize=16, fontweight="bold")
save_and_show(fig, "08b_subplots_gridspec.png")
