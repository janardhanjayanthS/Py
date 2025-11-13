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
    # word_arr: list[str] = [char.lower() for char in word if char != " "]
    # l, r = 0, len(word_arr) - 1
    # while l < r:
    #     if word_arr[l] != word_arr[r]:
    #         return False
    #     l += 1
    #     r -= 1

    # return True


if __name__ == "__main__":
    # print(is_palindrome("jana"))
    # print(is_palindrome("Madam"))
    # print(is_palindrome("nurses run"))
    ...
