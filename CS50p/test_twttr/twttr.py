def main():
    string = input("Input: ")
    print(f"Output: {shorten(string)}")



def shorten(word):
    for char in word:
        if char.upper() in ['A','I','O','U','E']:
            word = word.replace(char, '')
    return word


if __name__ == "__main__":
    main()