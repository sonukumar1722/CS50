import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    # TODO: Read database file into a variable
    database = []
    with open(sys.argv[1], "r") as dna:
        reader1 = csv.reader(dna)
        for row in reader1:
            database.append(row)

    # TODO: Read DNA sequence file into a variable
    sequence = ""
    with open(sys.argv[2], "r") as f:
        sequence = f.read()

    # TODO: Find longest match of each STR in DNA sequence
    # Storing STR sublist data of individuals
    str = database[0][1:]
    count = {}
    for c in str:
        count[c] = longest_match(sequence, c)
    # Extracts the values of Diffrents STR in form of list
    strcount = list(count.values())

    # TODO: Check database for matching profiles
    # Storing the name of the matching profiles
    name = ""
    with open(sys.argv[1], "r") as file:
        reader2 = csv.reader(file)
        # Skip the line
        next(reader2)
        for row in reader2:
            if strcount == row[1:]:
                name = row[0]
                break
            else:
                name = "No Match"
    print(name)

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return str(longest_run)


main()
