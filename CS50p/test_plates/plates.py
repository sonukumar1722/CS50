def main():
    plate = input("Plate: ")

    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")


def is_valid(s):
    if s[:2].isalpha() and 2 <= len(s) <= 6 and s.isalnum():
        for char in s[2:]:
            if char.isdigit():
                if s[s.index(char):].isdigit() and not s[s.index(char)] == '0':
                    return True
                else:
                    return False
            elif s.isalpha():
                return True
    else:
        return False

if __name__ == "__main__":
    main()