import statistics

marks = [78, 85, 90, 85, 92, 70, 85]

print("Marks:", marks)
print("Mean:", statistics.mean(marks))
print("Median:", statistics.median(marks))
print("Mode:", statistics.mode(marks))
print("Population standard deviation:", statistics.pstdev(marks))
print("Population variance:", statistics.pvariance(marks))
