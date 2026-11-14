import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 4))
months = ["Jan", "Feb", "Mar", "Apr", "May"]
rainfall = [12, 30, 45, 60, 110]
ax.plot(months, rainfall, marker="o", label="Rainfall")
ax.set_title("Monthly rainfall")
ax.set_xlabel("Month")
ax.set_ylabel("Rainfall (mm)")
ax.grid(True)
ax.legend()
plt.show()