import sys
import csv


def main():
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) < 3:
        print("Too few command-line arguments")
        sys.exit(1)
    elif len(sys.argv) > 3:
        print("Too many command-line arguments")
        sys.exit(2)
    # Check if the provided file names have the .csv extension
    elif not sys.argv[1].endswith(".csv") or not sys.argv[2].endswith(".csv"):
        print("Not a CSV file")
        sys.exit(3)
    else:
        # Call the read_from_file function with the input file name
        read_from_file(sys.argv[1])


def read_from_file(input_file):
    try:
        # Open the input file in read mode
        with open(input_file, "r") as file:
            # Create a CSV reader object
            reader = csv.DictReader(file)
            # Call the write_to_file function with the reader object
            write_to_file(reader)
    except FileNotFoundError:
        print("Could not read the file")
        sys.exit(4)


def write_to_file(reader):
    try:
        # Open the output file in write mode
        with open(sys.argv[2], "w", newline="") as file:
            # Create a CSV writer object
            writer = csv.DictWriter(file, fieldnames=["first", "last", "house"])
            # Write the header row to the output file
            writer.writeheader()
            # Process each row from the input file
            for row in reader:
                # Extract the full name and house from the row
                full_name, house = row["name"], row["house"]
                # Split the full name into last name and first name
                last_name, first_name = full_name.split(",")
                # Write the converted row to the output file
                writer.writerow({"first": first_name, "last": last_name, "house": house})
    except FileNotFoundError:
        print("Could not write to the file")
        sys.exit(5)


if __name__ == "__main__":
    main()
