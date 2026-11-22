import matplotlib.pyplot as plt
from common import apply_style, get_market_share, save_and_show

apply_style()
share = get_market_share()  # Fetches a dictionary (e.g., {'BrandA': 40, 'BrandB': 25, ...})
labels = list(share.keys())  # Extracts the category/brand names for text labels
sizes = list(share.values())  # Extracts numerical shares (proportions) for slice calculation

# Generates a single window/canvas containing 1 row and 2 side-by-side axes (ax1 and ax2)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))

# --- 1. Classic pie with an exploded slice ---
explode = [
    0.1,
    0,
    0,
    0,
    0,
]  # Dictates that the 1st slice is pushed outwards by 10% of the radius, while others remain flush
ax1.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%",  # Automatically calculates percentages and formats to one decimal place (e.g., '35.4%')
    explode=explode,  # Applies the separation array defined above
    startangle=90,  # Rotates the starting point of the first slice to the top (12 o'clock position)
    shadow=True,  # Applies a subtle 3D drop-shadow under the pie chart
    wedgeprops={
        "edgecolor": "white"
    },  # Passes a style dictionary to draw crisp white borders between slices
)
ax1.set_title("Smartphone Market Share")
ax1.axis("equal")  # Squashes distortion to ensure the chart renders as a true circle rather than an oval

# --- 2. Donut chart: a pie with a hole (wedge width < 1) ---
ax2.pie(
    sizes,
    labels=labels,
    autopct="%1.0f%%",  # Formats percentages as whole integers (e.g., '35%')
    startangle=90,
    pctdistance=0.8,  # Pushes the calculated percentage text outward closer to the outer rim (80% of radius)
    wedgeprops={
        "width": 0.4,
        "edgecolor": "white",
    },  # 'width': 0.4 slices out the center, leaving a thick ring that takes up 40% of the outer radius
)
ax2.text(
    0, 0, "2026", ha="center", va="center", fontsize=16, fontweight="bold"
)  # Places center text at (0,0) with horizontal and vertical alignment centered
ax2.set_title("Donut Chart Version")

save_and_show(
    fig, "04_pie_charts.png"
)  # Exports the combined dual-plot asset to a file layout
