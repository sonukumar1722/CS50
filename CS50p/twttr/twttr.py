string = input("Input: ")
for char in string:
    if char.upper() in ['A','I','O','U','E']:
       string = string.replace(char, '')
print(f"Output: {string}")
