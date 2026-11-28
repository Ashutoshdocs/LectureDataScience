import matplotlib.pyplot as plt  # Import the main plotting library (Matplotlib)
from common import (
    apply_style,
    get_monthly_sales,
    save_and_show,
)  # Import custom helper functions from a local 'common.py' module

apply_style()  # Apply a custom visual/aesthetic style to your matplotlib charts

df = (
    get_monthly_sales()
)  # Retrieve a pandas DataFrame containing monthly sales data

# Step 1: Look at raw numbers - can you spot the trend quickly?
print(
    "Raw data (hard to see patterns):"
)  # Print a section header to the console
print(
    df.to_string(index=False)
)  # Print the entire table without the row index numbers

# Step 2: Same data as a chart - trend is instantly visible
fig, ax = plt.subplots()  # Create a figure (canvas) and an axes (plot area) object

ax.plot(
    df["Month"],
    df["Electronics"],
    marker="o",
    label="Electronics",
)  # Plot 'Month' on X-axis, 'Electronics' on Y-axis with circle markers ('o') and a legend label
ax.plot(
    df["Month"],
    df["Clothing"],
    marker="s",
    label="Clothing",
)  # Plot 'Clothing' on Y-axis with square markers ('s') and a legend label
ax.plot(
    df["Month"],
    df["Groceries"],
    marker="^",
    label="Groceries",
)  # Plot 'Groceries' on Y-axis with triangle markers ('^') and a legend label

# Every good chart has: a title, axis labels, and a legend
ax.set_title(
    "Monthly Sales: A Chart Tells the Story Faster"
)  # Set the main title at the top of the chart
ax.set_xlabel("Month")  # Label the horizontal X-axis
ax.set_ylabel("Sales (in thousands)")  # Label the vertical Y-axis
ax.legend()  # Display the legend to match line colors/markers to category names

save_and_show(
    fig, "01_intro.png"
)  # Save the figure as an image file ('01_intro.png') and display it on screen
