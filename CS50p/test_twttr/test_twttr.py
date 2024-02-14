from twttr import shorten
import sys

def main():
    test_shorten()

def test_shorten():
    assert shorten("Twitter") == "Twttr"
    assert shorten("What's your name?") == "Wht's yr nm?"
    assert shorten("CS50") == "CS50"
    assert shorten("CSE Student") == "CS Stdnt"



if __name__ == "__main__":
    main()