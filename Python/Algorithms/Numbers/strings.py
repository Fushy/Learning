def is_palindrome_py(word):
    """Return True if word is a palindrome, False if not."""
    return word == word[::-1]


def is_palindrome_rec(word, i=0):
    if i + 1 > len(word) // 2:
        return True
    elif word[i] == word[-1 - i]:
        return is_palindrome_rec(word, i + 1)
    return False


if __name__ == '__main__':
    print(is_palindrome_rec(""))
    print(is_palindrome_rec("a"))
    print(is_palindrome_rec("aa"))
    print(is_palindrome_rec("foo"))
    print(is_palindrome_rec("racecar"))
    print(is_palindrome_rec("troglodyte"))
    print(is_palindrome_rec("civic"))
