def main():
    # prompts the user to take input
    fractions = convert("Fractions: ")
    print(fractions)


def convert(fraction):
    while True:
        try:
            operand1, operand2 = input(fraction).split('/')
            if int(operand1) > int(operand2):
                continue
            return gauge(int(operand1) * 100 / int(operand2))
        except ValueError:
            pass
        except ZeroDivisionError:
            pass

def gauge(percentage):
    if 0 <= percentage <= 1:
        return 'E'
    elif 99 <= percentage<= 100:
        return 'F'
    elif 1 < percentage < 100:
        return f'{round(percentage)}%'



if __name__ == "__main__":
    main()
