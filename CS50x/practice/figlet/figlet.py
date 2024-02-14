from pyfiglet import Figlet
from sys import argv, exit
import random

figlet = Figlet()
if len(argv) == 3 and (argv[2] not in figlet.getFonts() or argv[1] not in ['-f', '--font']):
    print("Invalid usage")
    exit(1)
elif len(argv) == 1:
    figlet.setFont(font=random.choice(figlet.getFonts()))
else:
    figlet.setFont(font=argv[2])


text = input("Input: ")
print("Output:")
print(figlet.renderText(text))
