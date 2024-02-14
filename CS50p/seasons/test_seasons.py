from seasons import life_spam
import pytest

def main():
    test_data()
    test_my_function_exits()


def test_date():
    assert life_spam("1999-01-01") == "Twelve million, eight hundred eighty-nine thousand, four hundred forty minutes"
    assert life_spam("1999-12-31") == "Twelve million, three hundred sixty-five thousand, two hundred eighty minutes"
    assert life_spam("2020-08-01") == "One million, five hundred thirty-seven thousand, nine hundred twenty minutes"
    assert life_spam("2008-01-12") == "Eight million, one hundred forty thousand, three hundred twenty minutes"


def test_my_function_exits():
    with pytest.raises(SystemExit):
        life_spam("January 1, 2000")

    with pytest.raises(SystemExit):
        life_spam("February 6th, 1998")


if __name__ == '__main__':
    main()