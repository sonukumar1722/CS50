import cs50
text = input().split()
for str in text:
    if str == ":)":
        print("🙂", end=" ")
    elif str == ":(":
        print("🙁", end=" ")
    else:
        print(str, end=" ")