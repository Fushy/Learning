def is_palindrome_py(word):
    """Return True if word is a palindrome, False if not."""
    return word == word[::-1]


def is_palindrome_rec(text):
    if len(text) <= 1:
        return True
    head = text[0]
    middle = text[1:-1]
    last = text[-1]
    return head == last and is_palindrome_rec(middle)


if __name__ == '__main__':
    print(is_palindrome_rec(""))
    print(is_palindrome_rec("a"))
    print(is_palindrome_rec("aa"))
    print(is_palindrome_rec("foo"))
    print(is_palindrome_rec("racecar"))
    print(is_palindrome_rec("troglodyte"))
    print(is_palindrome_rec("civic"))
