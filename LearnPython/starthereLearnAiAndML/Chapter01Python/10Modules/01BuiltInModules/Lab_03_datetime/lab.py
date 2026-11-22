from datetime import date, datetime, timedelta

today = date.today()
now = datetime.now()

print("Today's date:", today)
print("Current date and time:", now)
print("Formatted date:", now.strftime("%d-%m-%Y %H:%M"))

# Create a specific date.
joining_date = date(2024, 1, 15)
print("Joining year:", joining_date.year)
print("Joining month:", joining_date.month)

# Calculate a date 7 days from today.
next_week = today + timedelta(days=7)
print("Date after 7 days:", next_week)
