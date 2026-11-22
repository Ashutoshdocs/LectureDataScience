"""Reference solutions for exercises.py."""
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

CATS = ["Electronics", "Clothing", "Groceries"]


def ex01_line(sales):
    fig, ax = plt.subplots()
    ax.plot(sales["Month"], sales["Electronics"], marker="o")
    ax.set_title("Electronics")
    ax.set_xlabel("Month")
    ax.set_ylabel("Sales")
    return fig


def ex02_three_lines_legend(sales):
    fig, ax = plt.subplots()
    for cat in CATS:
        ax.plot(sales["Month"], sales[cat], label=cat)
    ax.legend()
    return fig


def ex03_annotate_peak(sales):
    fig, ax = plt.subplots()
    ax.plot(range(len(sales)), sales["Electronics"])
    i = int(sales["Electronics"].idxmax())
    ax.annotate("Peak", xy=(i, sales["Electronics"][i]), xytext=(i - 3, sales["Electronics"][i] + 5),
                arrowprops=dict(arrowstyle="->"))
    return fig


def ex04_sorted_barh(totals):
    fig, ax = plt.subplots()
    s = totals.sort_values()                      # barh draws bottom-up, so ascending puts the largest on top
    bars = ax.barh(s.index, s.values)
    ax.bar_label(bars)
    return fig


def ex05_grouped_bars(sales):
    df = sales.head(6)
    x = np.arange(len(df))
    w = 0.27
    fig, ax = plt.subplots()
    for offset, cat in zip([-w, 0, w], CATS):
        ax.bar(x + offset, df[cat], w, label=cat)
    ax.set_xticks(x, df["Month"])
    ax.legend()
    return fig


def ex06_stacked_bars(sales):
    df = sales.head(6)
    fig, ax = plt.subplots()
    bottom = np.zeros(len(df))
    for cat in CATS:
        ax.bar(df["Month"], df[cat], bottom=bottom, label=cat)
        bottom += df[cat].to_numpy()
    ax.legend()
    return fig


def ex07_donut(share):
    fig, ax = plt.subplots()
    ax.pie(list(share.values()), labels=list(share.keys()), wedgeprops={"width": 0.4})
    ax.text(0, 0, "Total", ha="center", va="center")
    return fig


def ex08_hist_mean(scores):
    fig, ax = plt.subplots()
    ax.hist(scores, bins=range(0, 101, 10), edgecolor="white")
    ax.axvline(scores.mean(), color="red", linestyle="--")
    return fig


def ex09_scatter_trend(df):
    fig, ax = plt.subplots()
    ax.scatter(df["study_hours"], df["score"], alpha=0.6)
    slope, intercept = np.polyfit(df["study_hours"], df["score"], 1)
    xs = np.linspace(df["study_hours"].min(), df["study_hours"].max(), 50)
    ax.plot(xs, slope * xs + intercept, color="red")
    ax.set_title(f"Study vs score (r = {df['study_hours'].corr(df['score']):.2f})")
    return fig


def ex10_subplots_shared(sales):
    fig, axes = plt.subplots(1, 3, sharey=True, figsize=(12, 4))
    for ax, cat in zip(axes, CATS):
        ax.plot(range(12), sales[cat])
        ax.set_title(cat)
    return fig


def ex11_log_scale():
    n = np.arange(1, 21)
    fig, ax = plt.subplots()
    ax.plot(n, 2.0 ** n)
    ax.set_yscale("log")
    return fig


def ex12_sns_box(df):
    fig, ax = plt.subplots()
    sns.boxplot(data=df, x="grade_level", y="score", order=["Freshman", "Sophomore", "Junior", "Senior"], ax=ax)
    return fig


def ex13_sns_heatmap(df):
    fig, ax = plt.subplots()
    sns.heatmap(df[["study_hours", "sleep_hours", "score"]].corr(), annot=True, vmin=-1, vmax=1, cmap="coolwarm", ax=ax)
    return fig


def ex14_sns_hue_scatter(df):
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x="study_hours", y="score", hue="gender", ax=ax)
    return fig


def ex15_declutter(sales):
    fig, ax = plt.subplots()
    ax.plot(sales["Month"], sales["Electronics"])
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title("Electronics sales keep growing", loc="left")
    ax.set_ylim(0, sales["Electronics"].max() * 1.1)
    return fig
