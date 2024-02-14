from jar import Jar
import pytest


def test_init():
    # Initialize a Jar object and check its capacity.
    jar = Jar()
    assert jar.capacity == 12


def test_str():
    # Check the string representation of the Jar object when it is empty.
    jar = Jar()
    assert str(jar) == ""

    # Check the string representation of the Jar object when it has 1 cookie.
    jar.deposit(1)
    assert str(jar) == "🍪"

    # Check the string representation of the Jar object when it is full.
    jar.deposit(11)
    assert str(jar) == "🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪"


def test_deposit():
    # Deposit 5 cookies into the Jar object and check its size.
    jar = Jar()
    jar.deposit(5)
    assert jar.size == 5

    # Deposit 6 cookies into the Jar object and check its size.
    jar.deposit(6)
    assert jar.size == 11

    # Try to deposit more cookies than the capacity of the Jar object.
    with pytest.raises(ValueError):
        jar.deposit(5)


def test_withdraw():
    # Deposit 5 cookies into the Jar object and check its size.
    jar = Jar()
    jar.deposit(5)
    assert jar.size == 5

    # Withdraw 2 cookies from the Jar object and check its size.
    jar.withdraw(2)
    assert jar.size == 3

    # Try to withdraw more cookies than the number of cookies in the Jar object.
    with pytest.raises(ValueError):
        jar.withdraw(6)
