from bank import value

def main():
    test_zero_value()
    test_hundread_value()
    test_twenty_value()


def test_zero_value():
    assert value("Hello, Newman") == 0
    assert value("Hello") == 0

def test_hundread_value():
    assert value("Godd morning") == 100
    assert value("What's happening?") == 100
    assert value("What’s up!") == 100

def test_twenty_value():
    assert value("How you doing?") == 20
    assert value("he..Ey you") == 20











if __name__ == "__main__":
    main()
