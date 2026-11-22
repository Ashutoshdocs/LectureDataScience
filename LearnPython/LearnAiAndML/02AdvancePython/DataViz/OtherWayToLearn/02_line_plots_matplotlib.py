import matplotlib.pyplot as plt
import numpy as np
from common import apply_style, get_monthly_sales, save_and_show

apply_style()
df = get_monthly_sales()

# --- Style 1: pyplot (quick, MATLAB-like) ---
plt.figure()  # Creates a new, blank window/canvas context
x = np.linspace(
    0, 10, 100
)  # Generates an array of 100 equally spaced numbers from 0 to 10
plt.plot(
    x, np.sin(x), label="sin(x)"
)  # Plots the sine wave (defaults to solid line) and labels it
plt.plot(
    x, np.cos(x), label="cos(x)", linestyle="--"
)  # Plots the cosine wave using a dashed line ('--')
plt.title("pyplot interface: sin and cos")  # Adds a title to the active plot
plt.xlabel("x")  # Labels the active horizontal axis
plt.ylabel("y")  # Labels the active vertical axis
plt.legend()  # Displays the legend using the provided labels
save_and_show(
    plt.gcf(), "02a_pyplot_basic.png"
)  # 'plt.gcf()' gets the Current Figure to save and show it

# --- Style 2: Object-Oriented (recommended for real projects) ---
fig, ax = (
    plt.subplots()
)  # Explicitly creates fig (canvas) and ax (the unique plot area)

# Format customization: color, linestyle, marker, linewidth
ax.plot(
    df["Month"],
    df["Electronics"],
    color="#1f77b4",
    linestyle="-",
    marker="o",
    linewidth=2,
    label="Electronics",
)  # Solid blue line with circle markers
ax.plot(
    df["Month"],
    df["Clothing"],
    color="#ff7f0e",
    linestyle="--",
    marker="s",
    linewidth=2,
    label="Clothing",
)  # Dashed orange line with square markers
ax.plot(
    df["Month"],
    df["Groceries"],
    color="#2ca02c",
    linestyle=":",
    marker="^",
    linewidth=2,
    label="Groceries",
)  # Dotted green line with triangle markers

# Annotate the highest point
best = (
    df["Electronics"].idxmax()
)  # Finds the row index where Electronics sales are at their maximum
ax.annotate(
    "Peak",  # The text string to display on the chart
    xy=(best, df["Electronics"][best]),  # Coordinates where the arrow points
    xytext=(
        best - 2,
        df["Electronics"][best] + 5,
    ),  # Coordinates where the text sits (shifted left and up)
    arrowprops=dict(
        arrowstyle="->"
    ),  # Configures a simple arrow pointing from text to data point
)

ax.set_title("Monthly Sales by Category (OO interface)")  # Set title on 'ax'
ax.set_xlabel("Month")  # Set x-label on 'ax'
ax.set_ylabel("Sales (in thousands)")  # Set y-label on 'ax'
ax.set_ylim(0, 90)  # Sets the vertical axis boundaries from 0 to 90
ax.legend(
    loc="lower right"
)  # Places the legend explicitly in the bottom right corner

save_and_show(fig, "02b_line_chart.png")  # Saves and renders this specific figure
