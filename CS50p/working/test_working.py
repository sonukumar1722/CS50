from working import convert
import pytest



def test_ValueError():
    # Test cases to verify that ValueError is raised for invalid input
    with pytest.raises(ValueError):
        convert("19:60 AM to 5:60")

    with pytest.raises(ValueError):
        convert("9 AM - 5 PM")

    with pytest.raises(ValueError):
        convert("09:00 AM - 17:00 PM")

    with pytest.raises(ValueError):
        convert("15:00 AM to 25:00 PM")


def test_start_time():
    # Test cases to verify the conversion of start time
    assert convert("10:30 PM to 8:50 AM") == "22:30 to 08:50"
    assert convert("10 PM to 8 AM") == "22:00 to 08:00"

def test_end_time():
    # Test cases to verify the conversion of end time
    assert convert("9:00 AM to 5:00 PM") == "09:00 to 17:00"
    assert convert("9 AM to 5 PM") == "09:00 to 17:00"


