import cs50

# Prompt user to input change it have


def get_cents():
    n = cs50.get_float("Change owed: ")
    while (n < 0):
        n = cs50.get_float("Change owed: ")
    return n * 100

# Calculate the number of quarter to give the customer


def calculate_quarters(cents):
    counter = 0
    while (cents > 24):
        cents -= 25
        counter += 1
    return counter

# Calculate the number of dimes to give the customer


def calculate_dimes(cents):
    counter = 0
    while (cents > 9):
        cents -= 10
        counter += 1
    return counter

# Calculate the number of nickels to give the customer


def calculate_nickels(cents):
    counter = 0
    while (cents > 4):
        cents -= 5
        counter += 1
    return counter

# Calculate the number of pennies to give the customer


def calculate_pennies(cents):
    return cents


# Ask how many cents the customer is owed
cents = get_cents()


# Calculate the number of quarters to give the customer
quarters = calculate_quarters(cents)
cents = cents - quarters * 25


# Calculate the number of dimes to give the customer
dimes = calculate_dimes(cents)
cents = cents - dimes * 10
# Calculate the number of nickels to give the customer
nickels = calculate_nickels(cents)
cents = cents - nickels * 5


# Calculate the number of pennies to give the customer
pennies = calculate_pennies(cents)
cents = cents - pennies * 1


# Sum coins
coins = quarters + dimes + nickels + pennies

# Prtotal number of coins to give the customer
print(int(coins))