from pyfiglet import Figlet
import sys
from random import choice


figlet = Figlet()
fonts = figlet.getFonts()

if len(sys.argv) == 3 and sys.argv[1] in ['-f', '--f'] and sys.argv[2] in fonts:
    txt = input("Input: ")
    figlet.setFont(font=sys.argv[2])
    print(figlet.renderText(txt))

elif len(sys.argv) == 1:
    txt = input("Input: ")
    figlet.setFont(font=choice(fonts))
    print(figlet.renderText(txt))

else:
    sys.exit("Invalid usage")