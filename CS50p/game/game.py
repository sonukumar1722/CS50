import random

# Prompt the user to enter the level and validate the input
level = input("Level: ")
while not level.isdigit():
    level = input("Level: ")
else:
    while not int(level) > 0:
        level = input("Level: ")

# Generate a random number within the specified level
rand_num = random.randint(1, int(level))

# Start the guessing game loop
while True:
    # Prompt the user to make a guess and validate the input
    guess = input("Guess: ")
    while not guess.isdigit():
        guess = input("Guess: ")
    else:
        while not int(guess) > 0:
            guess = input("Guess: ")

    guess = int(guess)

    # Compare the guess with the random number
    if guess < rand_num:
        print("Too small!")
        continue
    elif guess > rand_num:
        print("Too large!")
        continue
    else:
        print("Just right!")
        break
