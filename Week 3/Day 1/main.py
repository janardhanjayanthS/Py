def is_palindrome(word: str) -> bool:
    """
    Checks if a word is palindrome or not,
    excludes letter case and spaces

    Args:
        word: word to check palindrome

    Returns:
        bool: True if word is palindrome, False otherwise
    """
    cleaned = ''.join([char.lower() for char in word if char != ' '])
    return cleaned == cleaned[::-1]
