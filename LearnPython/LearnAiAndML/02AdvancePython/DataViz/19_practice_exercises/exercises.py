"""Visualization practice: fill in each function, then run:  python lecture.py exercises

Every function receives data and must RETURN the Matplotlib Figure it creates (do not call plt.show()).
The checker inspects the figure (number of lines/bars, titles, labels, limits...) to grade it.
Each docstring says exactly what is checked.
"""
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def ex01_line(sales):
    """01. One line of sales["Electronics"] vs sales["Month"] with circle markers ("o").
    Title "Electronics", x-label "Month", y-label "Sales"."""
    ...


def ex02_three_lines_legend(sales):
    """02. One line per column Electronics, Clothing, Groceries (in that order), each with label=<column name>,
    and a legend."""
    ...


def ex03_annotate_peak(sales):
    """03. Plot Electronics and use ax.annotate to add text "Peak" pointing at the maximum value
    (xy = (index of max, max value))."""
    ...


def ex04_sorted_barh(totals):
    """04. totals is a pandas Series (category -> number). Horizontal bars SORTED so the largest is at the TOP,
    with value labels (ax.bar_label)."""
    ...


def ex05_grouped_bars(sales):
    """05. Grouped bars for the first 6 months: Electronics, Clothing, Groceries side by side (3 bar containers,
    width 0.27), x tick labels = the month names, and a legend."""
    ...


def ex06_stacked_bars(sales):
    """06. STACKED bars for the first 6 months (Electronics at the bottom, then Clothing, then Groceries) using bottom=.
    The top of each stack must equal the monthly total."""
    ...


def ex07_donut(share):
    """07. share is a dict brand -> %. A donut chart: ax.pie with wedgeprops={"width": 0.4}, labels = brands,
    and the text "Total" in the centre (ax.text at 0, 0)."""
    ...


def ex08_hist_mean(scores):
    """08. Histogram of scores with bins=range(0, 101, 10) and a vertical dashed red line at the mean (ax.axvline)."""
    ...


def ex09_scatter_trend(df):
    """09. Scatter of df.study_hours (x) vs df.score (y), plus a straight trend line from np.polyfit (ax.plot).
    Title must contain "r = " followed by the correlation rounded to 2 decimals (e.g. "r = 0.89")."""
    ...


def ex10_subplots_shared(sales):
    """10. A 1x3 figure with sharey=True: one line per category (Electronics, Clothing, Groceries), with each Axes
    titled with its category name."""
    ...


def ex11_log_scale():
    """11. Plot y = 2**n for n = 1..20 on a LOG y-scale."""
    ...


def ex12_sns_box(df):
    """12. sns.boxplot of score by grade_level with order ["Freshman", "Sophomore", "Junior", "Senior"]."""
    ...


def ex13_sns_heatmap(df):
    """13. sns.heatmap of df[["study_hours", "sleep_hours", "score"]].corr() with annot=True and vmin=-1, vmax=1."""
    ...


def ex14_sns_hue_scatter(df):
    """14. sns.scatterplot of study_hours vs score with hue="gender" (the legend must show both genders)."""
    ...


def ex15_declutter(sales):
    """15. Line chart of Electronics with the TOP and RIGHT spines hidden, a LEFT-aligned title (loc="left"),
    and the y-axis starting at 0 (ax.set_ylim(0, ...))."""
    ...
