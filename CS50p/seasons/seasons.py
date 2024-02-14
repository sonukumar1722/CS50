from datetime import date, datetime
import sys
import re
import inflect



def main():
    # Prompt user for Date of Birth
    dob = input("Date of Birth: ")
    print(life_spam(dob))


def life_spam(dob):
    p = inflect.engine()

    # Check if the input matches the date format (YYYY-MM-DD)
    match = re.match(r"\d{4}-\d{2}-\d{2}", dob)

    if match:
        # Get today's date
        today = date.today()
        today = f"{today.year}-{today.month}-{today.day}"

        # Convert date strings to datetime objects
        date_of_birth = datetime.strptime(dob, "%Y-%m-%d")
        date_of_today = datetime.strptime(today, "%Y-%m-%d")

        # Calculate the difference between the two dates
        delta = date_of_today - date_of_birth

        # Calculate the total minutes
        minutes = round(delta.total_seconds() / 60)

        # Convert minutes to words using inflect
        minutes_in_words = p.number_to_words(minutes)

        # Format the output string
        return f"{minutes_in_words} minutes".capitalize().replace(' and', '')
    else:
        # If the input doesn't match the expected format, exit the program
        sys.exit(1)


if __name__ == "__main__":
    main()
