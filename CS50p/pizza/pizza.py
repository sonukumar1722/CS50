from tabulate import tabulate
import sys
import csv


def main():
    # Checks for the command-line arguments
    if len(sys.argv) < 2:
        print("Too few command_line arguments")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("Too many command-line arguments")
        sys.exit(2)
    # Checks for the CSV file
    elif not sys.argv[1].endswith('.csv'):
        print("Not a csv file")
        sys.exit(3)
    else:
        print(formate_to_table(sys.argv[1]))


# Foramte the csv file to table
def formate_to_table(file):
    menu = []
    try:
        with open(file, 'r') as f:
            # Create CSV reader object
            reader = csv.reader(f)
            for row in reader:
                menu.append(list(row))
        # return the tabulated formate of CSV file
        return tabulate(menu, headers="firstrow", tablefmt="grid")

    except FileNotFoundError:
        print("File not found")
        sys.exit(4)


if __name__ == "__main__":
    main()

