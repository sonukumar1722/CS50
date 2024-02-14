
def main():
    greet =  input("Greeting: ")
    print(f"${value(greet)}")

def value(greeting):
    greeting = greeting.lower().strip()
    if greeting.startswith("hello"):
        return 0
    elif greeting.startswith("h") and not greeting.startswith("hello"):
        return 20
    else:
        return 100


if __name__ == "__main__":
    main()