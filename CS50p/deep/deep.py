text =  (input("What is the Answer to the Great Question of Life, the Universe, and Everything? ")).strip()
if 'forty two' == text.lower() or 'forty-two' == text.lower() or '42' == text:
    print("Yes")
else:
    print("No")