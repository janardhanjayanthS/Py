from main import is_palindrome


def test_empty_string():
    """
    Test case for empty string
    """
    assert is_palindrome("") == True


def test_basic_palindrome():
    """
    Test cases for regular words
    """
    assert is_palindrome("ama") == True
    assert is_palindrome("monkey") == False


def test_case_sensitive_palindrome():
    """
    Test case for words with upper/lower cases
    """
    assert is_palindrome("Madam") == True
    assert is_palindrome("ManONAM") == True


def test_space_included_palindrome():
    """
    Test cases for words seperated by spaces
    """
    assert is_palindrome("nurses run") == True
    assert is_palindrome("random words here") == False
