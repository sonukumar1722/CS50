from plates import is_valid

def main():
    test_alpha()
    test_digits()
    test_alphanumeric()
    test_startswith_zero()
    test_special_characters()

def test_alpha():
    assert is_valid("CS50") == True

    assert is_valid("CS50P") == False
    assert is_valid("PI3.14") == False
    assert is_valid("OUTATIME") == False
    assert is_valid("H") == False

def test_alphanumeric():
    assert is_valid("AAA22A") == False
    assert is_valid("AAA222") == True

def test_startswith_zero():
    assert is_valid("CS05") == False
    assert is_valid("0CS05") == False

def test_digits():
    assert is_valid("3248") == False

def test_special_characters():
    assert is_valid("fsl$4@") == False






if __name__ == "__main__":
    main()
