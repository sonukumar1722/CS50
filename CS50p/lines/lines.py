from sys import argv, exit


def main():
    if len(argv) > 2:
        # Too many command-line arguments
        print("Too many command-line arguments")
        exit(1)
    elif len(argv) < 2:
        # Too few command-line arguments
        print("Too few command-line arguments")
        exit(2)
    elif not argv[1].endswith(".py"):
        # Not a python file
        print("Not a python file")
        exit(3)
    else:
        # Call the lines function to count lines in the file
        line_count = lines(argv[1])
        if line_count is not None:
            # Print the line count
            print(line_count)


def lines(file_name):
    count = 0
    try:
        with open(file_name, 'r') as file:
            lines = (line for line in file)
            # Skip lines starting with '#' or containing only whitespace
            count = sum(1 for line in lines if not line.lstrip().startswith("#") and not line.isspace())
    except FileNotFoundError:
        # File does not exist
        print("File does not exist")
    return count


if __name__ == '__main__':
    main()
