# Importing modules
import cs50
import math

# Calculate the length of the credit card number


def length(card_number):

    number = card_number
    counter = 0
    while (int(number) > 0):
        counter += 1
        number /= 10
    return counter


# Find the first two digits of credit card number
def starts_with(card_number):
    number = card_number
    lengt = length(number)
    start = number // int(math.pow(10, lengt - 2))
    return int(start)


# Checks the validition of the credit card


def checksum(card_number):
    number = card_number
    copy = card_number
    sum = term = 0
    while (int(copy) > 0):
        sum += copy % 10
        copy //= 10
        term = (int(copy) % 10) * 2
        if (term > 9):
            while (int(term) > 9):
                sum += term % 10
                term //= 10
        sum = sum + int(term)
        copy //= 10
    if (sum % 10 == 0):
        return True
    else:
        return False


if __name__ == '__main__':
    
    # Prompts the user for the credit card number
    number = cs50.get_int("Number: ")
    valid = checksum(number)
    while (number == False):
        number = cs50.get_int("Number: ")
        valid = checksum(number)

    lengt = length(number)
    start = starts_with(number)

    if (valid and lengt == 15 and (start == 34 or start == 37)):
        print("AMEX\n")

    elif (valid and lengt == 16 and (start == 51 or start == 52 or start == 53 or start == 54 or start == 55)):
        print("MASTERCARD\n")

    elif (valid and (lengt == 13 or lengt == 16) and int((start / 10)) == 4):
        print("VISA\n")

    else:
        print("INVALID\n")
