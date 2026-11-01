"""
04 - Pie Charts in Matplotlib
-----------------------------
Covers: basic pie, percentages (autopct), explode, shadow, startangle,
and donut charts. Use pies only for parts of a whole (few categories).
"""

import matplotlib.pyplot as plt
from common import apply_style, get_market_share, save_and_show

apply_style()
share = get_market_share()
labels = list(share.keys())
sizes = list(share.values())

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))

# --- 1. Classic pie with an exploded slice ---
explode = [0.1, 0, 0, 0, 0]  # pull out the first slice
ax1.pie(sizes, labels=labels, autopct="%1.1f%%", explode=explode,
        startangle=90, shadow=True,
        wedgeprops={"edgecolor": "white"})
ax1.set_title("Smartphone Market Share")
ax1.axis("equal")  # keeps it a circle

# --- 2. Donut chart: a pie with a hole (wedge width < 1) ---
ax2.pie(sizes, labels=labels, autopct="%1.0f%%", startangle=90,
        pctdistance=0.8, wedgeprops={"width": 0.4, "edgecolor": "white"})
ax2.text(0, 0, "2026", ha="center", va="center", fontsize=16, fontweight="bold")
ax2.set_title("Donut Chart Version")

save_and_show(fig, "04_pie_charts.png")
