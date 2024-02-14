text = input("Greeting: ")
text = text.strip()
if text.startswith(('hello', 'Hello')):
    print("$0")
elif text.startswith(('h','H')) and not text.startswith(('hello' or'Hello')):
    print('$20')
else:
    print("$100")