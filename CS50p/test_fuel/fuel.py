def main():
    # prompts the user to take input
    percent = convert(input("Fractions: "))
    print(f'{gauge(percent)}')


def convert(fraction):
    while True:
        try:
            operand1, operand2 = fraction.split('/')
            num1 = int(operand1)
            num2 = int(operand2)
            return num1 * 100 / num2
        except ValueError:
            raise ValueError
        except ZeroDivisionError:
            raise ZeroDivisionError


def gauge(percentage):
    if 0 <= percentage <= 1:
        return 'E'
    elif 99 <= percentage <= 100:
        return 'F'
    elif 1 < percentage < 99:
        return f'{round(percentage)}%'



if __name__ == "__main__":
    main()
