from cs50 import get_int

# Promts user for pyramid height
height = get_int("Height: ")
while(height < 1 or height > 8):
    height = int(input("Height: "))

# Iteration i for rows
for i in range(1, height + 1):
    # Iteration j for columns
    for j in range(height, i, -1):
        print(" ", end='')
    # Iteration k for left pyramid hashes
    for k in range(i):
        print("#", end='')
    print("  ", end='')
    # Iteration k for right pyramid hashes
    for l in range(i):
        print("#", end='')
    print()
