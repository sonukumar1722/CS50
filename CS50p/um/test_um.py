from um import count

def test_catch():
    # Check if 'um' appears only once in the given string
    assert count('um') == 1

    # Check if 'um' appears only once in the given string
    assert count('Um, thanks for the album.') == 1

    # Check if 'um' appears twice in the given string
    assert count('Um, thanks, um...') == 2

    # Check if 'um' does not appear in the given string
    assert count('Yummy') == 0

    # Check if 'um' does not appear in the given string
    assert count('Thnaks, for the yum... food.') == 0
