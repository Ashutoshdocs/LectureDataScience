"""
01 - Introduction to Data Visualization
---------------------------------------
Why visualize? The same numbers are hard to read in a table but obvious in a chart.
This demo prints raw data, then shows it as a chart so you can compare.
"""

import matplotlib.pyplot as plt
from common import apply_style, get_monthly_sales, save_and_show

apply_style()
df = get_monthly_sales()

# Step 1: Look at raw numbers - can you spot the trend quickly?
print("Raw data (hard to see patterns):")
print(df.to_string(index=False))

# Step 2: Same data as a chart - trend is instantly visible
fig, ax = plt.subplots()
ax.plot(df["Month"], df["Electronics"], marker="o", label="Electronics")
ax.plot(df["Month"], df["Clothing"], marker="s", label="Clothing")
ax.plot(df["Month"], df["Groceries"], marker="^", label="Groceries")

# Every good chart has: a title, axis labels, and a legend
ax.set_title("Monthly Sales: A Chart Tells the Story Faster")
ax.set_xlabel("Month")
ax.set_ylabel("Sales (in thousands)")
ax.legend()

save_and_show(fig, "01_intro.png")
