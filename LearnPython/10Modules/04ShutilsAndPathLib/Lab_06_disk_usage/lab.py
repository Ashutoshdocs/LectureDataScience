import shutil

usage = shutil.disk_usage(".")

print("Total bytes:", usage.total)
print("Used bytes :", usage.used)
print("Free bytes :", usage.free)

# Optional: display values in GiB.
gib = 1024 ** 3
print("Total GiB:", round(usage.total / gib, 2))
print("Free GiB :", round(usage.free / gib, 2))
