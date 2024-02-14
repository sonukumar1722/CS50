import fuel
import pytest

def main():
    test_gauge()
    test_convert()
    test_error()


def test_convert():
    assert fuel.convert("0/4") == 0
    assert fuel.convert("1/4") == 25
    assert fuel.convert("1/2") == 50
    assert fuel.convert("3/4") == 75
    assert fuel.convert("4/4") == 100

def test_error():
    with pytest.raises(ZeroDivisionError):
        fuel.convert("1/0")
    with pytest.raises(ValueError):
        fuel.convert("cat/dog")

def test_gauge():
    assert fuel.gauge(1) == 'E'
    assert fuel.gauge(99) == 'F'
    assert fuel.gauge(55) == '55%'
    assert fuel.gauge(35) == '35%'

if __name__ == "__main__":
    main()