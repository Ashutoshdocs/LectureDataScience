"""Lecture 19 — Project: a week of weather data with parallel arrays and masks."""
import numpy as np

days = np.array(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
max_c = np.array([31.2, 33.8, 35.1, 36.4, 34.0, 29.5, 30.8])
rain_mm = np.array([0, 0, 2.5, 0, 12.0, 30.5, 4.0])

max_f = max_c * 9 / 5 + 32
print("In Fahrenheit:", max_f.round(1))
print("Hottest:", days[max_c.argmax()], max_c.max(), "C")
print("Above average:", days[max_c > max_c.mean()])
print("Biggest day-to-day drop:", np.diff(max_c).min().round(1), "C")
print("Rainy days:", days[rain_mm > 0])
print("Total rain:", rain_mm.sum(), "mm")
print("Hot AND dry:", days[(max_c > 33) & (rain_mm == 0)])

print("\n--- Extensions ---")
print("Rain over 5 mm:", days[rain_mm > 5])
print("Weekly average:", max_f.mean().round(1), "F")
labels = np.select([max_c > 34, max_c > 30], ["hot", "warm"], default="cool")
print("Labels:", dict(zip(days.tolist(), labels.tolist())))
print("Biggest rise on:", days[np.diff(max_c).argmax() + 1])
print("Running rain total:", np.cumsum(rain_mm))
moving = np.convolve(max_c, np.ones(3) / 3, mode="valid")
print("3-day moving avg :", moving.round(2), "(centred on", days[1:-1], ")")
