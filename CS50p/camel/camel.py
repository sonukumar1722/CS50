string = input("camelCase: ")
snake_case = ''
for str in string:
    if str.isupper():
        print("_",end='')
        snake_case += f"_"
    snake_case += str
print("snake_case: ", snake_case.lower())