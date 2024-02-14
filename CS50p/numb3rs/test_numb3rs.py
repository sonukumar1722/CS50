import pytest
from numb3rs import validate

def main():
    test_validate()

def test_valid():
    # Test valid IP addresses
    assert validate("127.0.0.1") == True
    assert validate("255.255.255.255") == True

    # Test invalid IP addresses
    assert validate("512.512.512.512") == False
    assert validate("1.2.3.1000") == False
    assert validate("999.2.3.1000") == False
    assert validate("99.271.321.432") == False

    # Test non-IP input
    assert validate("cat") == False


if __name__ == "__main__":
    main()
