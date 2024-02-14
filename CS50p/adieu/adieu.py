def main():
    # Create an empty list to store names
    names = []

    # Loop until an EOFError occurs (this condition is incorrect and should be revised)
    while True:
        try:
                prompt = input("Name: ")
                names.append(prompt)

        except EOFError:
            break

    # Handle the EOFError
    length = len(names)

    # Check if there is exactly one name in the list
    if length == 1:
      farewell_message =  f"Adieu, adieu, to {' '.join(names)}"

    # Check if there are exactly two names in the list
    elif length == 2:
        farewell_message = f"Adieu, adieu, to {' and '.join(names)}"

    # Check if there are more than two names in the list
    elif length > 2:
        names = ', '.join(names).split()
        names.insert(length - 1, 'and')
        farewell_message = f"Adieu, adieu, to {' '.join(names)}"

    print(farewell_message)

if __name__ == "__main__":
    main()
