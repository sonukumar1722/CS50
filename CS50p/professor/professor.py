import random

def main():
    # Prompt the user for the level
    level = get_level()
    score = 0

    # Generate and solve 10 math problems
    for _ in range(10):
        x = generate_integer(level)
        y = generate_integer(level)
        problem = f"{x} + {y} = "

        # Give the user up to 3 tries to solve each problem
        for _ in range(3):
            response = input(problem)

            if is_numeric(response):
                # Check if the user's answer is correct
                if int(response) == x + y:
                    score += 1
                    break
                else:
                    # Incorrect answer, display error message
                    print("EEE")
            else:
                # Invalid input, display error message
                print("EEE")

        else:
            # Display the correct answer after 3 incorrect tries
            print(f"Correct answer: {x + y}")
    # Display the user's score
    print(f"Score: {score}")


def get_level():
    # Prompt the user for the level until a valid input is provided
    while True:
        level = input("Level: ")
        if level in ['1', '2', '3']:
            return int(level)


def generate_integer(level):
    # Generate a random integer based on the chosen level
    if level == 1:
        return random.randint(0, 9)
    elif level == 2:
        return random.randint(10, 99)
    elif level == 3:
        return random.randint(100, 999)


def is_numeric(string):
    # Check if a string can be converted to an integer
    try:
        int(string)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    main()
