import re
import sys


def main():
    # Prompt the user to enter a text
    print(count(input("Text: ")))


def count(s):
    # Define the pattern to match 'um' followed by a punctuation mark or end of word
    pattern = r"\bum(\,|\.|\?|)\b"

    # Find all matches of the pattern in the input text (case-insensitive)
    matches = re.findall(pattern, s.lower())

    # Return the count of matches found
    return len(matches)


if __name__ == "__main__":
    # Call the main function to start the program
    main()
