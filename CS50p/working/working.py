import re
import sys


def main():
    # Prompt user for input and print the converted result
    print(convert(input("Hours: ")))


def convert(s):
    # Use regular expression to match the input pattern
    match = re.match(r"^(\d{1,2})(:\d{1,2}|) (AM|PM) to (\d{1,2})(:\d{1,2}|) (AM|PM)$", s)

    if not match:
        raise ValueError("Invalid input")

    # Extract hour, minute, and AM/PM for the start time and end time
    hour1, minute1, am_pm1 = match.groups()[:3]
    hour2, minute2, am_pm2 = match.groups()[3:]

    # Convert hour1 and hour2 to integers
    hour1 = int(hour1)
    hour2 = int(hour2)

    # If minutes are provided, convert them to integers
    if minute1 != "" or minute2 != "":
        minute1 = int(minute1.replace(":", ""))
        minute2 = int(minute2.replace(":", ""))
    else:
        minute1 = minute2 = 0



    # Check if the hour and minute values are within the valid range
    if not (0 <= hour1 <= 12 and 0 <= hour2 <= 12 and 0 <= minute1 <= 59 and 0 <= minute2 <= 59):
        raise ValueError("Out-of-range time")

    # Convert the hours to 24-hour format if necessary
    hour1 = am_pm(hour1, am_pm1)
    hour2 = am_pm(hour2, am_pm2)

    # Format the converted time as a string and return it
    return f"{hour1:02}:{minute1:02} to {hour2:02}:{minute2:02}"


def am_pm(hour, am_pm):
    # Convert the hour to 24-hour format based on AM/PM
    if am_pm == "PM" and hour != 12:
        hour += 12
    elif am_pm == "AM" and hour == 12:
        hour = 0
    return hour


if __name__ == "__main__":
    main()
